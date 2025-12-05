import streamlit as st
import requests
import time

# API Configuration
API_URL = "http://localhost:5000"

# Page config
st.set_page_config(
    page_title="AutoCDA - AI Circuit Design Assistant",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f9fafb;
    }
    
    /* Hero section */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Input section */
    .input-label {
        font-size: 1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    /* Example dropdown styling */
    .stSelectbox label {
        font-weight: 600;
        color: #374151;
    }
    
    /* Generate button */
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.125rem;
        transition: background-color 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    
    /* Output card */
    .output-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    
    /* Success message */
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Character counter */
    .char-counter {
        text-align: right;
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Download button styling */
    .download-button {
        background-color: #10b981;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
    }
    
    .download-button:hover {
        background-color: #059669;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<h1 class="hero-title">⚡ AutoCDA</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">AI Circuit Design Assistant - Convert natural language into working KiCad schematics</p>', unsafe_allow_html=True)

st.markdown("---")

# Example selector
st.markdown('<p class="input-label">💡 Try an Example (Optional)</p>', unsafe_allow_html=True)

examples = {
    "Select an example...": "",
    "RC Low-Pass Filter (1kHz)": "Design a low-pass RC filter with a cutoff frequency of 1 kHz",
    "RC High-Pass Filter (1kHz)": "Design a high-pass RC filter with a cutoff frequency of 1 kHz",
    "Voltage Divider (9V to 5V)": "Create a voltage divider that converts 9V input to 5V output",
    "RC Low-Pass Filter (500Hz)": "Design a low-pass RC filter with 500 Hz cutoff",
    "Voltage Divider (12V to 3.3V)": "Design a voltage divider from 12V to 3.3V"
}

selected_example = st.selectbox(
    "Choose a pre-filled example",
    options=list(examples.keys()),
    label_visibility="collapsed"
)

# Input Section
st.markdown('<p class="input-label">📝 Circuit Description</p>', unsafe_allow_html=True)

# Pre-fill if example selected
default_text = examples[selected_example] if selected_example != "Select an example..." else ""

user_input = st.text_area(
    "Describe your circuit in plain English",
    value=default_text,
    height=150,
    max_chars=500,
    placeholder="Example: Design a 2-stage RC low-pass filter with 1 kHz cutoff frequency",
    label_visibility="collapsed"
)

# Character counter
char_count = len(user_input)
st.markdown(f'<p class="char-counter">{char_count}/500 characters</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Generate Button
generate_clicked = st.button("🚀 Generate Circuit", type="primary", use_container_width=True)

# Output Section - Connected to Backend API
if generate_clicked:
    if not user_input.strip():
        st.error("⚠️ Please enter a circuit description before generating.")
    else:
        with st.spinner("🔧 Designing your circuit... This may take 5-10 seconds."):
            try:
                # Make API request
                response = requests.post(
                    f"{API_URL}/generate",
                    json={"description": user_input},
                    timeout=30
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        # Display success message
                        st.success("✅ Circuit generated successfully!")
                        
                        # Display explanation
                        st.markdown("### 📋 Design Explanation")
                        explanation = result.get('explanation', 'Circuit generated.')
                        
                        # Split explanation into parts for better formatting
                        if "Calculations:" in explanation:
                            parts = explanation.split("Calculations:")
                            # Display description part
                            st.info(parts[0].strip())
                            
                            # Display calculations in a code block for better readability
                            if len(parts) > 1:
                                calc_parts = parts[1].split("\n\n", 1)
                                st.markdown("**Calculations:**")
                                st.code(calc_parts[0].strip(), language="")
                                
                                # Display remaining text
                                if len(calc_parts) > 1:
                                    st.info(calc_parts[1].strip())
                        else:
                            st.info(explanation)
                        
                        # Download button
                        st.markdown("### 📥 Download KiCad Project")
                        download_url = f"{API_URL}{result.get('download_url')}"
                        filename = result.get('filename', 'circuit.zip')
                        
                        try:
                            file_response = requests.get(download_url, timeout=10)
                            if file_response.status_code == 200:
                                # Determine button label and instructions based on file type
                                if filename.endswith('.zip'):
                                    button_label = "📦 Download KiCad Project (ZIP)"
                                    instructions = """
                                    **📖 How to open in KiCad:**
                                    
                                    1. **Download and extract** the ZIP file to a folder
                                    2. **Open KiCad** application
                                    3. Click **File → Open Project**
                                    4. Navigate to the extracted folder
                                    5. Select **`circuit.kicad_pro`** file and click Open
                                    6. In the project window, double-click **Schematic Editor** (or click the icon)
                                    7. You'll see your components (R1, C1, etc.) placed on the schematic!
                                    
                                    **✨ Your circuit components are ready!** The schematic shows all components with their values.
                                    
                                    💡 **Note:** Components are placed but not connected yet. You can:
                                    - Add wires manually using the wire tool (W key)
                                    - Or use **Tools → Update PCB from Schematic** to generate the PCB layout
                                    """
                                else:
                                    button_label = "📦 Download KiCad Netlist"
                                    instructions = "Import this netlist file into KiCad using File → Import → Netlist"
                                
                                st.download_button(
                                    label=button_label,
                                    data=file_response.content,
                                    file_name=filename,
                                    mime="application/zip" if filename.endswith('.zip') else "application/octet-stream",
                                    use_container_width=True
                                )
                                st.markdown(instructions)
                            else:
                                st.error("Failed to prepare download file.")
                        except Exception as e:
                            st.error(f"Download preparation failed: {str(e)}")
                    else:
                        st.error(f"❌ {result.get('error', 'Unknown error occurred')}")
                else:
                    try:
                        error_data = response.json()
                        st.error(f"❌ {error_data.get('error', 'Request failed')}")
                    except:
                        st.error(f"❌ Request failed with status code {response.status_code}")
                
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The server might be busy. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to the server. Make sure the backend is running at http://localhost:5000")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    <p>Built with ❤️ for IDEATHON 2025 | <a href="https://github.com/yourusername/autocda" target="_blank" style="color: #2563eb;">View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
