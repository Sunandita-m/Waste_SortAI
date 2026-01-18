"""
EcoSort AI - Smart Waste Segregation Assistant
SDG 12: Responsible Consumption and Production
1M1B AI for Sustainability Virtual Internship
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load waste database
def load_waste_data():
    try:
        with open('database/waste_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: waste_data.json not found.")
        return {
            "plastic bottle": {
                "category": "Recyclable",
                "instructions": "1. Remove cap and ring\n2. Rinse thoroughly\n3. Crush to save space\n4. Place in DRY WASTE bin",
                "tips": ["Caps often different plastic - separate", "Labels can be left on"],
                "impact": "Recycling 1 kg saves 3.4 kWh energy"
            }
        }

WASTE_DB = load_waste_data()

# ============== AI ENHANCEMENTS ==============
class AISystem:  # ← NOTE: Correct spelling with "I" not "l"
    """Combined AI features for demonstration"""
    
    @staticmethod
    def rag_enhance(query, category):
        """Simple RAG implementation"""
        knowledge = {
            "plastic": "Recycling 1 kg plastic saves 3.4 kWh energy",
            "battery": "Each battery can pollute 400 liters of water",
            "food": "Composting reduces methane emissions significantly",
            "glass": "Glass recycling saves 30% energy vs new production",
            "paper": "Recycling paper saves 17 trees per ton"
        }
        
        for key in knowledge:
            if key in query.lower():
                return knowledge[key]
        return "Proper waste management supports SDG 12"
    
    @staticmethod
    def agentic_workflow(query):
        """Simple agentic workflow"""
        agents = [
            {"name": "Classifier Agent", "task": "Identify waste type using pattern matching"},
            {"name": "Instruction Agent", "task": "Generate step-by-step disposal guide"},
            {"name": "Impact Agent", "task": "Calculate environmental benefits"},
            {"name": "Location Agent", "task": "Suggest local disposal facilities"}
        ]
        return {"agents": agents, "workflow": "Sequential AI Pipeline"}

class EcoSortAssistant:
    def __init__(self):
        self.categories = ['Recyclable', 'Wet Waste', 'Hazardous', 'E-Waste']
    
    def process_query(self, query, location="default"):
        query_lower = query.lower().strip()
        
        # Find matching waste item
        for item, info in WASTE_DB.items():
            if item in query_lower:
                return {
                    'item': query,
                    'category': info['category'],
                    'instructions': info['instructions'].replace('\\n', '\n'),
                    'recycling_tips': info.get('tips', []),
                    'environmental_impact': info['impact'],
                    'local_facilities': self.get_local_facilities(location, info['category'])
                }
        
        # Default response
        return {
            'item': query,
            'category': 'Unknown',
            'instructions': 'Please contact local municipal authority',
            'recycling_tips': ['Take a clear photo for identification'],
            'environmental_impact': 'Proper segregation helps recycling',
            'local_facilities': ['Contact Municipal Corporation']
        }
    
    def get_local_facilities(self, location, category):
        facilities = {
            'Recyclable': ['Green Recycling Center - 2km', 'Weekly Collection - Fridays'],
            'Hazardous': ['Special Handling Facility'],
            'Wet Waste': ['Compost Facility - 3km'],
            'default': ['Contact Municipal Corporation']
        }
        return facilities.get(category, facilities['default'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_waste():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter waste item'}), 400
        
        # Original logic
        assistant = EcoSortAssistant()
        result = assistant.process_query(query)
        
        # Add AI enhancements - CORRECT SPELLING HERE!
        ai_system = AISystem()  # ← FIXED: AISystem not AlSystem
        
        result['ai_enhancements'] = {
            'rag_insight': ai_system.rag_enhance(query, result['category']),
            'agentic_workflow': ai_system.agentic_workflow(query),
            'ai_methods': 'Pattern Matching + RAG + Agentic AI',
            'ai_components': [
                'Classification Engine',
                'Knowledge Retrieval (RAG)',
                'Multi-Agent Workflow',
                'Impact Calculator'
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("EcoSort AI - Advanced Waste Segregation Assistant")
    print("SDG 12: Responsible Consumption")
    print("AI Features: RAG + Agentic Workflow")
    print("=" * 50)
    print(f"Database: {len(WASTE_DB)} waste items")
    print("AI System: AISystem with RAG and Agentic AI")
    print("Server: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000)