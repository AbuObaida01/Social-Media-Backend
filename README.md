# FastAPI Authentication API

A production-ready backend API built using FastAPI, PostgreSQL, and JWT-based authentication.
This project focuses on secure authentication, clean architecture, database migrations, and deployment.

The API is fully deployed and uses Alembic for database version control.

## Live API

### Base URL:
https://fastapi-learning-x6jm.onrender.com

### Interactive API Docs (Swagger UI):
https://fastapi-learning-x6jm.onrender.com/docs

## Features

• FastAPI modular project structure with routers
• PostgreSQL database integration
• SQLAlchemy ORM models
• Pydantic request/response validation
• User registration with hashed password storage
• Secure login using OAuth2 password flow
• JWT access token generation (HS256)
• Token expiration handling
• Protected routes using dependency injection
• Authentication using Authorization Bearer tokens
• Alembic database migrations
• Production deployment on Render

## Tech Stack

FastAPI
PostgreSQL
SQLAlchemy
Alembic
OAuth2 (Password Flow)
JWT (HS256)
python-jose
passlib (bcrypt)
pydantic-settings
Uvicorn

## Authentication Flow

User registers with email and password

Password is hashed before storing in the database

User logs in using OAuth2 password flow

Server validates credentials

Server generates a JWT containing user_id

Client sends token in Authorization header

Protected routes verify the token and extract user information

## Project Structure

app/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── config.py
├── oauth2.py
├── routers/
│ ├── auth.py
│ ├── users.py
│ └── posts.py

alembic/

## Environment Variables

Create a .env file in the project root:

DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

The .env file is ignored and not committed to GitHub.

Running Locally

### Clone the repository

Create and activate a virtual environment

### Install dependencies

pip install -r requirements.txt

Configure your .env file

Run database migrations

alembic upgrade head

### Start the server

uvicorn app.main:app --reload

### Production Deployment

The application is deployed on Render.

## Production start command:

alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 10000

Migrations run automatically during deployment.

### Database Migrations

This project uses Alembic for database version control.

### Create a new migration:

alembic revision --autogenerate -m "message"

### Apply migrations:

alembic upgrade head

## Current Status

Authentication and authorization are fully implemented.
The project structure supports extension with features such as relationships, voting systems, pagination, testing, and rate limiting.

## Notes

This project was built while studying backend development with FastAPI, with emphasis on:

• Security best practices
• Clean architecture
• Proper environment management
• Production deployment workflow
• Database migration management
• Proper Understanding of APIs
• Role Based User Access