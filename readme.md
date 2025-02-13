# Drift

Drift is an AI-powered application that learns your travel preferences through interactive questions and predicts your future holiday destinations. The app uses a Flask backend and a PostgreSQL database, and it is containerized using Docker and Docker Compose.

## Features

- Interactive questionnaire to gather user preferences
- Machine learning model to predict future holiday destinations
- Flask backend for handling requests and running the AI model
- PostgreSQL database for storing user responses
- Docker and Docker Compose for easy deployment

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/drift.git
   cd drift
   ```

2. Build and start the services using Docker Compose:

   ```sh
   docker-compose build
   docker-compose up
   ```

3. Access the app at `http://localhost:5000`.

### Usage

1. Start the app and navigate to `http://localhost:5000`.
2. Answer the questions to provide your travel preferences.
3. The app will learn from your responses and predict future holiday destinations.