# E-Commerce API

<img width="2400" height="1600" alt="architecture_diagram" src="https://github.com/user-attachments/assets/65d8e44d-90bc-4ab4-a297-a425e6ecb06a" />

A modern e-commerce API built with FastAPI and MongoDB.

## Project Structure

```
├── core/                  # Configuration & Database
│   ├── config.py          # Application settings
│   ├── database.py        # MongoDB client setup
│   └── logging.py         # Logging configuration
├── models/                # MongoDB data models
│   ├── base.py            # Common types and base models
│   ├── product.py         # Product model
│   ├── order.py           # Order model
│   └── user.py            # User model (optional)
├── schemas/               # Pydantic validation schemas
│   ├── common.py          # Shared schemas
│   ├── product.py         # Product schemas
│   ├── order.py           # Order schemas
│   └── pagination.py      # Pagination schemas
├── routes/                # API endpoints
│   ├── __init__.py        # Router initialization
│   ├── product.py         # Product routes
│   ├── order.py           # Order routes
│   └── health.py          # Health check routes
├── services/              # Business logic
│   ├── product_service.py # Product service
│   └── order_service.py   # Order service
├── utils/                 # Helper functions
│   ├── pagination.py      # Pagination utilities
│   ├── bson_utils.py      # MongoDB ObjectId utilities
│   └── errors.py          # Error handling
├── main.py                # Application entry point
├── requirements.txt       # Project dependencies
└── .env.example           # Environment variables example
```
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/7522e5ae-5f44-4d31-b5ee-679c353a45d1" />

## Features

- Product management (CRUD operations)
- Order processing with inventory validation
- Pagination and filtering
- Error handling
- MongoDB integration with Motor (async)
- Data validation with Pydantic

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your environment variables
5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json

## MongoDB Setup

1. Install MongoDB or use MongoDB Atlas
2. Update the `MONGODB_URL` in your `.env` file

## Development

To run tests:
```bash
pytest
```

## License

MIT 
