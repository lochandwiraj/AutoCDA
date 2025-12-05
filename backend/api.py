from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import uuid
from datetime import datetime
import traceback
import zipfile
from dotenv import load_dotenv

# Load environment variables from .env file in parent directory
# override=True ensures .env values take precedence over system env vars
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path, override=True)

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from intent_extractor import IntentExtractor
from dsl_generator import generate_dsl_from_json
from circuit_validator import validate_circuit
from skidl_generator import SKiDLGenerator
from file_manager import FileManager
from explainer import generate_circuit_explanation
from input_validator import validate_user_input
from error_handler import InputValidationError, NLPError, GenerationError, ValidationError, CircuitError

app = Flask(__name__)
CORS(app)

# Use absolute path for output directory (parent directory of backend)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output_api')
OUTPUT_DIR = os.path.abspath(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize components
intent_extractor = IntentExtractor()
skidl_generator = SKiDLGenerator()
file_manager = FileManager(output_dir=OUTPUT_DIR)


@app.route('/generate', methods=['POST'])
def generate_circuit():
    try:
        # Get user input
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing circuit description'
            }), 400
        
        # Validate input
        try:
            user_input = validate_user_input(data['description'])
        except InputValidationError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        
        # Generate unique ID for this request
        request_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_prefix = f"circuit_{timestamp}_{request_id}"
        
        # Step 1: Extract circuit intent using NLP
        try:
            circuit_json = intent_extractor.extract_circuit_intent(user_input)
            if not circuit_json:
                raise NLPError("Failed to extract circuit intent")
            
            # Normalize circuit_json structure for explainer
            # Convert "circuit_type" to "type" and add "_filter" suffix if needed
            if "circuit_type" in circuit_json:
                circuit_type = circuit_json["circuit_type"]
                # Map short names to full names
                type_mapping = {
                    "rc_lowpass": "rc_lowpass_filter",
                    "rc_highpass": "rc_highpass_filter",
                    "voltage_divider": "voltage_divider"
                }
                circuit_json["type"] = type_mapping.get(circuit_type, circuit_type)
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Could not understand circuit description. Please be more specific about the circuit type and parameters.'
            }), 400
        
        # Step 2: Generate DSL
        try:
            dsl_string = generate_dsl_from_json(circuit_json)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to generate circuit representation: {str(e)}'
            }), 500
        
        # Step 3: Validate circuit
        try:
            is_valid, messages = validate_circuit(circuit_json)
            if not is_valid:
                error_msgs = [msg.message for msg in messages if msg.level.value == "ERROR"]
                if error_msgs:
                    return jsonify({
                        'success': False,
                        'error': 'Circuit validation failed:\n• ' + '\n• '.join(error_msgs)
                    }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Validation error: {str(e)}'
            }), 500
        
        # Step 4: Generate SKiDL code
        try:
            skidl_code = skidl_generator.dsl_to_skidl(dsl_string)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to generate circuit code: {str(e)}'
            }), 500
        
        # Step 5: Execute SKiDL and create netlist
        try:
            success, netlist_path, error = file_manager.execute_skidl(skidl_code, output_prefix)
            if not success:
                raise GenerationError(error)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to generate netlist: {str(e)}'
            }), 500
        
        # Step 6: Convert to KiCad schematic
        try:
            success, kicad_path, error = file_manager.convert_to_kicad(netlist_path)
            if not success:
                raise GenerationError(error)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to create KiCad schematic: {str(e)}'
            }), 500
        
        # Step 7: Generate explanation
        try:
            explanation = generate_circuit_explanation(circuit_json, dsl_string)
        except Exception as e:
            # Non-critical failure - provide basic explanation
            explanation = f"Generated circuit with {len(circuit_json.get('components', []))} components."
        
        # Get the directory containing the files
        file_dir = os.path.dirname(kicad_path)
        folder_name = os.path.basename(file_dir)
        
        # Create ZIP file with all KiCad project files
        zip_filename = f"circuit_{request_id}.zip"
        zip_path = os.path.join(file_dir, zip_filename)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add all relevant files to the ZIP
                for filename in ['circuit.net', 'circuit.kicad_pro', 'circuit.kicad_sch', 'circuit.py']:
                    file_path = os.path.join(file_dir, filename)
                    if os.path.exists(file_path):
                        zipf.write(file_path, filename)
        except Exception as e:
            print(f"Warning: Failed to create ZIP file: {e}")
            # Fall back to single file download
            zip_filename = 'circuit.net'
        
        # Success response
        return jsonify({
            'success': True,
            'explanation': explanation,
            'download_url': f'/download/{folder_name}/{zip_filename}',
            'filename': zip_filename,
            'request_id': request_id
        }), 200
    
    except CircuitError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected error: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please try again or contact support.'
        }), 500


@app.route('/download/<folder>/<filename>', methods=['GET'])
def download_file(folder, filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, folder, filename)
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Download failed: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


# Day 16: Competitive Positioning & Storytelling Routes
from backend.competitive_analysis import get_competitive_comparison, get_elevator_pitch
from backend.demo_script import get_demo_script
from backend.qa_responses import get_all_qa_pairs, search_qa


@app.route('/api/competitive-analysis', methods=['GET'])
def competitive_analysis():
    """
    Returns competitive landscape and differentiation
    """
    try:
        data = get_competitive_comparison()
        return jsonify({
            "success": True,
            "data": data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/elevator-pitch', methods=['GET'])
def elevator_pitch():
    """
    Returns 30-second elevator pitch
    """
    try:
        pitch = get_elevator_pitch()
        return jsonify({
            "success": True,
            "pitch": pitch
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/demo-script', methods=['GET'])
def demo_script():
    """
    Returns structured demo script with timing
    """
    try:
        script = get_demo_script()
        return jsonify({
            "success": True,
            "script": script
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/qa-database', methods=['GET'])
def qa_database():
    """
    Returns all Q&A pairs
    """
    try:
        qa_pairs = get_all_qa_pairs()
        return jsonify({
            "success": True,
            "qa_pairs": qa_pairs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/qa-search', methods=['POST'])
def qa_search_route():
    """
    Search Q&A database by keyword
    """
    try:
        data = request.json
        keyword = data.get('keyword', '')
        results = search_qa(keyword)
        return jsonify({
            "success": True,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("Starting AutoCDA API server...")
    print("API will be available at http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
