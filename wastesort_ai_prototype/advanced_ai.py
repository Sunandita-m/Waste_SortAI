"""
Advanced AI Features for EcoSort AI
Including RAG and Agentic AI workflows
"""

import json
import re
from typing import List, Dict, Any

class AdvancedEcoSortAI:
    """Combined RAG + Agentic AI system"""
    
    def __init__(self):
        self.rag_system = RAGSystem()
        self.agent_orchestrator = AgentOrchestrator()
        self.context_memory = []
    
    def process_with_ai(self, query: str) -> Dict[str, Any]:
        """Full AI pipeline with RAG and Agentic workflows"""
        
        # Step 1: Context retrieval (RAG)
        context = self.rag_system.retrieve_context(query)
        
        # Step 2: Agentic processing
        agent_results = self.agent_orchestrator.process(query, context)
        
        # Step 3: Response generation
        response = self.generate_response(query, agent_results, context)
        
        # Step 4: Learning (simple memory)
        self.learn_from_interaction(query, response)
        
        return {
            **response,
            "ai_features": {
                "rag_used": True,
                "agents_used": len(agent_results),
                "context_retrieved": len(context),
                "workflow": "RAG → Agentic → Generation → Learning"
            }
        }
    
    def generate_response(self, query, agent_results, context):
        """Generate final response combining all AI outputs"""
        return {
            "query": query,
            "primary_category": agent_results.get("primary_category", "Unknown"),
            "confidence_score": agent_results.get("confidence", 0.75),
            "step_by_step_guide": self.format_instructions(agent_results),
            "environmental_impact": self.calculate_impact(agent_results),
            "additional_insights": context[:3],  # Top 3 RAG results
            "ai_explanation": "This response combines RAG-retrieved knowledge with specialized AI agents."
        }
    
    def learn_from_interaction(self, query, response):
        """Simple learning mechanism"""
        self.context_memory.append({
            "query": query,
            "response": response["primary_category"],
            "timestamp": "2024-01-01"  # Use datetime in real implementation
        })
        if len(self.context_memory) > 100:  # Keep only recent 100
            self.context_memory.pop(0)


class RAGSystem:
    """Retrieval-Augmented Generation System"""
    
    def __init__(self):
        self.documents = self.load_documents()
        self.embeddings_cache = {}
    
    def load_documents(self):
        """Load waste management documents for retrieval"""
        return [
            {"id": 1, "text": "Plastic recycling reduces crude oil consumption", "topic": "recycling"},
            {"id": 2, "text": "Composting creates natural fertilizer", "topic": "composting"},
            {"id": 3, "text": "E-waste contains valuable metals", "topic": "e-waste"},
            {"id": 4, "text": "Batteries require special disposal", "topic": "hazardous"},
            {"id": 5, "text": "SDG 12 targets responsible consumption", "topic": "sustainability"},
            {"id": 6, "text": "Paper recycling saves trees", "topic": "recycling"},
            {"id": 7, "text": "Glass is infinitely recyclable", "topic": "recycling"},
            {"id": 8, "text": "Food waste in landfills produces methane", "topic": "composting"},
        ]
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant documents for the query"""
        query_terms = set(re.findall(r'\b\w+\b', query.lower()))
        
        relevant_docs = []
        for doc in self.documents:
            doc_terms = set(re.findall(r'\b\w+\b', doc["text"].lower()))
            if query_terms.intersection(doc_terms):
                relevant_docs.append(doc["text"])
        
        # Return top K relevant documents
        return relevant_docs[:top_k] if relevant_docs else [
            "Proper waste management contributes to sustainable development"
        ]


class AgentOrchestrator:
    """Orchestrates multiple specialized AI agents"""
    
    def __init__(self):
        self.agents = {
            "waste_classifier": WasteClassifierAgent(),
            "instruction_generator": InstructionGeneratorAgent(),
            "impact_calculator": ImpactCalculatorAgent(),
            "sdg_analyzer": SDGAnalyzerAgent()
        }
    
    def process(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Process query through all agents"""
        results = {}
        
        # Run each agent
        results["classification"] = self.agents["waste_classifier"].classify(query)
        results["instructions"] = self.agents["instruction_generator"].generate(
            results["classification"], context
        )
        results["impact"] = self.agents["impact_calculator"].calculate(
            results["classification"]
        )
        results["sdg_alignment"] = self.agents["sdg_analyzer"].analyze(
            results["classification"]
        )
        
        return {
            **results,
            "primary_category": results["classification"].get("category"),
            "confidence": results["classification"].get("confidence", 0.7)
        }


class WasteClassifierAgent:
    """Specialized agent for waste classification"""
    
    def classify(self, query: str) -> Dict[str, Any]:
        keywords_to_category = {
            "plastic": "Recyclable", "paper": "Recyclable", "glass": "Recyclable",
            "metal": "Recyclable", "food": "Wet Waste", "organic": "Wet Waste",
            "battery": "Hazardous", "chemical": "Hazardous", "medicine": "Hazardous",
            "electronic": "E-Waste", "mobile": "E-Waste", "laptop": "E-Waste"
        }
        
        query_lower = query.lower()
        for keyword, category in keywords_to_category.items():
            if keyword in query_lower:
                return {
                    "category": category,
                    "matched_keyword": keyword,
                    "confidence": 0.9,
                    "method": "keyword_matching"
                }
        
        return {"category": "General Waste", "confidence": 0.5}


class InstructionGeneratorAgent:
    """Agent for generating disposal instructions"""
    
    def generate(self, classification: Dict, context: List[str]) -> List[str]:
        category = classification.get("category", "General Waste")
        
        templates = {
            "Recyclable": [
                "Clean and dry the item thoroughly",
                "Remove any non-recyclable components",
                "Check local recycling guidelines",
                "Place in appropriate recycling bin"
            ],
            "Wet Waste": [
                "Use compostable bags only",
                "Keep separate from dry waste",
                "Dispose daily to prevent odor",
                "Consider home composting"
            ],
            "Hazardous": [
                "Do not mix with regular waste",
                "Use original container if safe",
                "Take to authorized facility",
                "Follow safety precautions"
            ],
            "E-Waste": [
                "Delete personal data first",
                "Remove batteries if possible",
                "Use authorized e-waste channels",
                "Consider repair before disposal"
            ]
        }
        
        return templates.get(category, [
            "Check municipal guidelines",
            "Contact local waste management",
            "Ensure safe handling"
        ])


class ImpactCalculatorAgent:
    """Agent for calculating environmental impact"""
    
    def calculate(self, classification: Dict) -> Dict[str, Any]:
        category = classification.get("category", "General Waste")
        
        impacts = {
            "Recyclable": {
                "energy_saved": "30-95%",
                "resources_conserved": "Reduces mining/extraction",
                "emissions_reduced": "Lower carbon footprint"
            },
            "Wet Waste": {
                "methane_reduction": "25x less than landfill",
                "fertilizer_created": "Natural compost",
                "soil_improvement": "Enhances soil quality"
            },
            "Hazardous": {
                "pollution_prevented": "Soil/water protection",
                "health_benefits": "Reduced exposure risk",
                "ecosystem_protection": "Wildlife safety"
            }
        }
        
        return impacts.get(category, {
            "general_impact": "Proper disposal has positive environmental effects"
        })


class SDGAnalyzerAgent:
    """Agent for analyzing SDG alignment"""
    
    def analyze(self, classification: Dict) -> List[str]:
        category = classification.get("category", "General Waste")
        
        sdg_mapping = {
            "Recyclable": ["SDG 12.5", "SDG 12.4", "SDG 9.4", "SDG 13.3"],
            "Wet Waste": ["SDG 12.3", "SDG 2.4", "SDG 13.2", "SDG 15.3"],
            "Hazardous": ["SDG 12.4", "SDG 3.9", "SDG 6.3", "SDG 14.1"],
            "E-Waste": ["SDG 12.5", "SDG 9.4", "SDG 8.4", "SDG 17.7"]
        }
        
        return sdg_mapping.get(category, ["SDG 12: Responsible Consumption"])


# Export the main AI system
ai_system = AdvancedEcoSortAI()