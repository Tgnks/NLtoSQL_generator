from typing import List, Dict
import re

class QueryUnderstanding:
    def __init__(self):
        pass

    def extract_entities(self, query: str) -> Dict[str, List[str]]:
        entities = {}
        # Example regex patterns for entity extraction
        patterns = {
            'date': r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD format
            'time': r'\b\d{1,2}:\d{2}\b',      # HH:MM format
            'location': r'\b(?:New York|Los Angeles|Chicago)\b',  # Example locations
            'product': r'\b(?:product1|product2|product3)\b'  # Example products
        }

        for entity, pattern in patterns.items():
            matches = re.findall(pattern, query)
            if matches:
                entities[entity] = matches

        return entities

    def identify_business_intent(self, query: str) -> str:
        # Simple keyword-based intent identification
        if "order" in query.lower():
            return "Order"
        elif "cancel" in query.lower():
            return "Cancel"
        elif "inquire" in query.lower():
            return "Inquiry"
        else:
            return "Unknown"

    def process_query(self, query: str) -> Dict[str, List[str]]:
        intent = self.identify_business_intent(query)
        entities = self.extract_entities(query)
        return {
            'intent': intent,
            'entities': entities
        }