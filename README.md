# Dream100 Project

## Overview

The Dream100 project is an implementation of the Dream100 strategy, a marketing approach that focuses on identifying and building relationships with 100 key influencers in a specific market. This application automates and enhances the process by:

1. Managing influencers and their associated web properties
2. Retrieving content from various platforms (currently focusing on YouTube)
3. Processing and embedding content for semantic search
4. Enabling users to find relevant content to engage with influencers effectively

## Quick Start

1. Clone the repository and navigate to the project directory
2. Set up a virtual environment and install dependencies: 
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```
3. Set up the PostgreSQL database with pgvector extension
4. Create a `.env` file with necessary environment variables (see Configuration section)
5. Run the application: `python run_app.py`
6. Access the application at `http://localhost:5173`

## Features

- Influencer management
- Automatic discovery of influencer web properties (website, Facebook, Instagram, YouTube, LinkedIn)
- YouTube transcript retrieval and processing
- Content chunking and embedding for semantic search
- Project-based organization of influencers
- RESTful API for frontend integration

Current Status:
- Fully Implemented: Influencer management, YouTube content retrieval, content embedding
- In Development: Web scraping for other platforms, follower analysis, topic analysis

## Technology Stack

- Backend: Python, FastAPI, SQLAlchemy, pgvector
- Frontend: React, Vite, Tailwind CSS, DaisyUI
- Database: PostgreSQL
- Embedding: FlagEmbedding (BAAI/bge-small-en-v1.5 model)

## Project Structure

```
dream100/
├── frontend/               # React frontend
├── dream100/               # Core Python package
│   ├── models/             # SQLAlchemy models
│   ├── context/            # Database context managers
│   ├── services/           # Business logic services
│   ├── utilities/          # Utility functions
│   └── db_config.py        # Database configuration
├── dream100_api/           # FastAPI application
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic schemas
│   └── auth/               # Authentication logic
├── tests/                  # Test suite
└── config.py               # Configuration settings
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 13+ with pgvector extension
- Node.js 14+

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dream100.git
   cd dream100
   ```

2. Set up a virtual environment and install backend dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements-dev.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

4. Set up the database:
   - Create a PostgreSQL database
   - Install the pgvector extension: `CREATE EXTENSION vector;`
   - Initialize the database schema:
     ```
     python -c "from dream100.db_config import init_db, create_session; _, engine = create_session(); init_db(engine)"
     ```

5. Create a `.env` file in the root directory (see Configuration section for details)

### Running the Application

To start both the backend and frontend servers, use the `run_app.py` script:

```
python run_app.py
```

This script will start the FastAPI backend server and the frontend development server concurrently.

Access the application at `http://localhost:5173`

## Development

### Adding New Features

1. Create or modify models in `dream100/models/`
2. Update context managers in `dream100/context/`
3. Implement business logic in `dream100/services/`
4. Create or update API routes in `dream100_api/routers/`
5. Define Pydantic schemas in `dream100_api/schemas/`
6. Implement frontend components and services

### Running Tests

Use pytest to run the test suite:

```
pytest
```

The test suite uses fixtures defined in `tests/conftest.py` for setup and teardown.

### Code Style and Linting

This project follows the PEP 8 style guide for Python code. We use the following tools for code quality:

- `black` for code formatting
- `flake8` for style guide enforcement
- `isort` for import sorting

Run these tools before committing your changes:

```
black .
isort .
flake8
```

## Configuration

The project uses a combination of `config.py` and environment variables for configuration. Create a `.env` file in the root directory with the following content:

```
DATABASE_URL=postgresql://username:password@localhost:5432/dream100
API_KEY=your_secret_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id
```

Additional configuration options can be found and modified in `config.py`.

## API Documentation

The API documentation is automatically generated using Swagger UI. Once the application is running, you can access the API docs at:

```
http://localhost:8000/docs
```

This interactive documentation allows you to explore and test the API endpoints.

## Deployment

1. Set up a production-ready PostgreSQL database with pgvector extension
2. Configure environment variables for production settings
3. Build the frontend:
   ```
   cd frontend
   npm run build
   ```
4. Serve the backend using a production ASGI server like Gunicorn:
   ```
   gunicorn dream100_api.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
5. Serve the frontend build directory using a web server like Nginx

## Security Considerations

- Never commit `.env` files or any files containing sensitive information to version control
- Use environment variables for all sensitive configuration in production
- Regularly update dependencies to patch security vulnerabilities
- Implement proper authentication and authorization in the application
- Use HTTPS in production to encrypt data in transit

## Troubleshooting

Common issues and solutions:

1. Database connection errors:
   - Ensure PostgreSQL is running and the DATABASE_URL is correct in your `.env` file
   - Verify that the pgvector extension is installed in your database

2. API key errors:
   - Double-check that all required API keys are correctly set in your `.env` file

3. Frontend build issues:
   - Ensure you have the latest LTS version of Node.js installed
   - Try deleting the `node_modules` folder and running `npm install` again

If you encounter any other issues, please check the existing GitHub issues or create a new one.

## Future Enhancements

- Implement web scraping for other social media platforms
- Add follower analysis for influencers
- Implement topic analysis on influencer content
- Expand market research capabilities
- Integrate with email or social media APIs for automated outreach

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.