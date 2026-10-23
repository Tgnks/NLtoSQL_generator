# NLtoSQL Generator

This project implements an Natural language to SQL Query generator using open-source technologies. The architecture is designed to handle user queries, classify intents, generate SQL queries, and manage responses effectively.

## Project Structure

```
ai-contact-center
├── src
│   ├── app.py                     # Entry point of the application
│   ├── api_gateway                 # API Gateway functionalities
│   │   ├── authentication.py       # User authentication and authorization
│   │   ├── session_management.py    # User session and conversation management
│   │   └── validation.py           # Input validation functions
│   ├── orchestration               # Orchestration of AI processes
│   │   ├── intent_classification.py # Intent classification logic
│   │   ├── query_understanding.py   # Query understanding and entity extraction
│   │   ├── retrieval                # Information retrieval methods
│   │   │   ├── semantic_search.py   # Semantic search functionality
│   │   │   ├── vector_search.py     # Vector-based search capabilities
│   │   │   └── hybrid_search.py     # Combined search methods
│   │   ├── context_selection.py     # Context selection for SQL generation
│   │   ├── sql_generation.py        # SQL query generation
│   │   ├── sql_validation.py        # SQL query validation
│   │   ├── error_correction.py      # Error correction and retry logic
│   │   └── response_generation.py    # Response generation based on SQL results
│   ├── database                     # Database schema and queries
│   │   ├── schema.sql               # SQL schema definition
│   │   └── queries.sql              # Predefined SQL queries
│   └── utils                        # Utility functions
│       └── logging.py               # Logging utilities
├── tests                            # Unit tests for the application
│   ├── test_api_gateway.py          # Tests for API gateway functionalities
│   ├── test_orchestration.py        # Tests for orchestration components
│   └── test_utils.py                # Tests for utility functions
├── requirements.txt                 # Project dependencies
├── README.md                        # Project documentation
└── .gitignore                       # Files to ignore in version control
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd ai-contact-center
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   - Execute the SQL schema in your database management system.
   - Load any predefined queries if necessary.

4. **Run the application**:
   ```
   python src/app.py
   ```

## Usage Guidelines

- The application exposes an API for user interactions. You can authenticate users, manage sessions, and process queries through the API endpoints.
- Ensure that the necessary environment variables and configurations are set up for the application to function correctly.

## Architecture Overview

The architecture consists of an API Gateway that handles authentication, session management, and input validation. The LangGraph Orchestration Workflow processes user intents, retrieves relevant information, generates SQL queries, and manages responses. The system is designed to be modular, allowing for easy updates and enhancements.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
