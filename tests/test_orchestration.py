import unittest
from src.orchestration.intent_classification import classify_intent
from src.orchestration.query_understanding import extract_entities
from src.orchestration.sql_generation import generate_sql

class TestOrchestration(unittest.TestCase):

    def test_classify_intent(self):
        query = "What is the status of my order?"
        expected_intent = "order_status"
        result = classify_intent(query)
        self.assertEqual(result, expected_intent)

    def test_extract_entities(self):
        query = "Show me the details of order 12345"
        expected_entities = {"order_id": "12345"}
        result = extract_entities(query)
        self.assertEqual(result, expected_entities)

    def test_generate_sql(self):
        context = {
            "table": "orders",
            "columns": ["order_id", "status"],
            "conditions": {"order_id": "12345"}
        }
        expected_sql = "SELECT order_id, status FROM orders WHERE order_id = '12345';"
        result = generate_sql(context)
        self.assertEqual(result.strip(), expected_sql.strip())

if __name__ == '__main__':
    unittest.main()