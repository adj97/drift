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

## Solution Design

## API endpoints & methods

- **Data Collection:** The /answer endpoint now accepts a justification field along with the question and answer.
- **Data Preprocessing:** The train_model function combines the question and justification into a single text feature and vectorizes it using TF-IDF.
- **Model Training:** The model is trained on the vectorized text data and saved to a file.
- **Making Predictions:** The /predict endpoint uses the trained model and vectorizer to make predictions based on new questions and justifications.

## Application Lifecycle

1. _Collect Text Responses_ - Modify your app to accept and store text responses (justifications) along with the answers to the questions.

2. _Preprocess Text Data_ - Convert the text responses into a format suitable for machine learning. This involves text cleaning, tokenization, and vectorization.

3. _Feature Extraction_ - Extract meaningful features from the text data using techniques like TF-IDF (Term Frequency-Inverse Document Frequency) or word embeddings (e.g., Word2Vec, GloVe).

4. _Integrate with Existing Data_ - Combine the extracted features from text responses with the existing structured data (e.g., answers to questions).

5. _Train the Model_ - Train a machine learning model on the combined dataset to improve its understanding of user preferences.

6. _Make Predictions_ - Use the trained model to make more accurate predictions based on both structured data and text responses.