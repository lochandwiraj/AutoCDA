"""
Pre-written Q&A responses for common questions
"""

QA_DATABASE = {
    "complex_circuits": {
        "question": "How does it handle complex multi-stage circuits?",
        "answer": "Current MVP focuses on single-stage circuits. Multi-stage designs are on the roadmap with hierarchical DSL representation."
    },
    
    "nlp_accuracy": {
        "question": "What if the NLP misinterprets the description?",
        "answer": "System validates circuits and shows explanations. Users can see exactly what was understood and catch any misinterpretations."
    },
    
    "component_values": {
        "question": "How accurate are component values?",
        "answer": "Values calculated using standard formulas (e.g., f_c = 1/(2πRC)) and rounded to E12/E24 series. Accuracy within 5%."
    },
    
    "vs_existing": {
        "question": "Why not use existing EDA tools?",
        "answer": "AutoCDA starts from pure natural language - no schematic needed. It's complementary to tools like KiCad, not a replacement."
    },
    
    "simulation": {
        "question": "Can I simulate the generated circuits?",
        "answer": "Yes! Circuits include voltage sources and are ready for simulation in KiCad/Ngspice immediately after generation."
    },
    
    "pcb_layout": {
        "question": "What about PCB layout?",
        "answer": "PCB automation is the next step. We generate schematics with connectivity - spatial routing is future work."
    }
}

def print_qa_cheatsheet():
    print("=" * 80)
    print("AUTOCDA Q&A CHEATSHEET")
    print("=" * 80)
    for key, qa in QA_DATABASE.items():
        print(f"\nQ: {qa['question']}")
        print(f"A: {qa['answer']}")
        print("-" * 80)

if __name__ == "__main__":
    print_qa_cheatsheet()
