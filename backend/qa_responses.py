"""
Structured Q&A responses for judge questions
"""

QA_DATABASE = {
    "complex_circuits": {
        "question": "How does it handle complex multi-stage circuits?",
        "answer": "Great question. The current MVP focuses on single-stage circuits to prove the concept. For multi-stage designs, the system would need hierarchical DSL representation, which is definitely on the roadmap. Right now, a user could generate each stage separately and manually connect them, but full automation of complex topologies is a future milestone.",
        "duration_seconds": 30,
        "strategy": "Acknowledge limitation, show future thinking, bridge to working features"
    },
    "nlp_accuracy": {
        "question": "What if the NLP misinterprets the circuit description?",
        "answer": "We handle this through validation and explainability. The system validates the generated circuit against basic electrical rules and shows the user exactly what it understood. If the interpretation seems wrong, the explanation makes it obvious—for example, if it calculated a 10kΩ resistor but you expected 1kΩ, you'd see the formula and catch the discrepancy.",
        "duration_seconds": 30,
        "strategy": "Turn limitation into feature (explainability as safety net)"
    },
    "existing_tools": {
        "question": "Why not use tool X instead?",
        "answer": "Tools like EasyEDA have AI features, but they typically assist with existing designs or PCB layout. AutoCDA is unique because it starts from pure natural language—no schematic needed. It's focused on the earliest design stage: translating intent into a first draft. It's complementary to existing tools, not a replacement.",
        "duration_seconds": 30,
        "strategy": "Acknowledge competitors, emphasize unique value proposition"
    },
    "component_accuracy": {
        "question": "How accurate are the component values?",
        "answer": "Component values are calculated using standard electrical formulas—for example, RC filters use fc = 1/(2πRC). The system then rounds to standard E12 or E24 series values, just like an engineer would. In testing, theoretical vs. actual cutoff frequencies match within 5%, which is typical for real-world component tolerances.",
        "duration_seconds": 30,
        "strategy": "Show technical rigor, quantify accuracy"
    },
    "analog_digital": {
        "question": "Can this handle analog and digital circuits?",
        "answer": "The current version focuses on analog passive circuits because they have well-defined formulas. Digital circuits require logic synthesis, which is a different problem space. That said, the architecture is extensible—the DSL could be expanded to include digital components, and the SKiDL library supports them. It's definitely a future direction.",
        "duration_seconds": 30,
        "strategy": "Honest about scope, show path forward"
    },
    "pcb_layout": {
        "question": "What about PCB layout?",
        "answer": "PCB layout is the natural next step. The groundwork is there—we already generate schematics with connectivity information. The challenge is automating component placement and routing, which requires spatial reasoning beyond just circuit topology. That's a significant research problem but absolutely on the roadmap.",
        "duration_seconds": 25,
        "strategy": "Acknowledge difficulty, show understanding of problem"
    },
    "safety": {
        "question": "How do you ensure the generated circuits are safe?",
        "answer": "Safety is built into the validation layer. The system checks for common issues like floating nodes, unrealistic voltage levels, and component ratings. For power circuits, we'd need additional rules—current limits, thermal constraints, etc. The MVP prioritizes low-voltage signal circuits, but the validation framework is designed to be extensible for safety-critical applications.",
        "duration_seconds": 30,
        "strategy": "Show care about safety, explain current vs future state"
    },
    "business_model": {
        "question": "What's the business model?",
        "answer": "There are several paths: a freemium SaaS with advanced features, API access for engineering teams, or integration with component suppliers for referral fees. The core value is saving engineering time—if we can compress hours into seconds, there's clear ROI for professional users. The MVP is open-source to validate demand.",
        "duration_seconds": 30,
        "strategy": "Show sustainability thinking, multiple options"
    },
    "simulation": {
        "question": "Does it run circuit simulations?",
        "answer": "The current MVP generates simulation-ready netlists that can be opened in KiCad and simulated with Ngspice. Automated simulation with result visualization is on the immediate roadmap. The foundation is there—we have the netlist format—we just need to add the testbench generation and plotting layer.",
        "duration_seconds": 25,
        "strategy": "Show what works now, clear path to full feature"
    },
    "learning_curve": {
        "question": "Who is the target user?",
        "answer": "Three groups: beginners learning circuit design without EDA expertise, engineers doing rapid prototyping who want to skip manual schematic entry, and educators who can use the explainability feature to teach circuit fundamentals. The system meets users where they are—natural language—and guides them to working designs.",
        "duration_seconds": 30,
        "strategy": "Specific user personas, clear value for each"
    }
}

def get_qa_response(question_key: str) -> dict:
    """
    Get structured response for a question key
    """
    return QA_DATABASE.get(question_key, {
        "answer": "That's a great question. Let me think about that...",
        "strategy": "Buy time, then bridge to known strengths"
    })

def get_all_qa_pairs():
    """
    Returns all Q&A pairs for study
    """
    return QA_DATABASE

def search_qa(keyword: str) -> list:
    """
    Search Q&A database by keyword
    """
    results = []
    keyword_lower = keyword.lower()
    
    for key, data in QA_DATABASE.items():
        if keyword_lower in data['question'].lower() or keyword_lower in data['answer'].lower():
            results.append({
                "key": key,
                "question": data['question'],
                "answer": data['answer']
            })
    
    return results

def export_qa_study_guide(filepath: str = "qa_study_guide.json"):
    """
    Export Q&A to JSON for study
    """
    import json
    with open(filepath, 'w') as f:
        json.dump(QA_DATABASE, f, indent=2)
    return filepath
