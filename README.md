# Book Shelf API

## Overview
The **Book Shelf API** is a simple, robust web service that allows users to manage their personal bookshelf. Users can add books, track which ones they've read, and mark which ones they liked. The API is built with **Python Flask**, stores data in a **MySQL** database, and is containerized using **Docker** for easy deployment and scalability.

## Features
- **Add books to the shelf**: Users can add books with details like title, author, and publication year.
- **Track read status**: Users can mark books as "read" or "unread."
- **Mark liked books**: Users can tag books they liked for future reference.
- **Persistent data storage**: The API stores data in a MySQL database for durability.
- **Scalable and portable**: The application is containerized using Docker for easy deployment.

## Technologies
- **Python (Flask)**: The back-end API is built using Flask, a lightweight web framework for Python.
- **MySQL**: A relational database to store book information, user preferences, and status.
- **Docker**: Containerizes the application and its dependencies, allowing for easy deployment across environments.

## Architecture
1. **Flask API**: Handles all HTTP requests and interacts with the MySQL database.
2. **MySQL Database**: Stores books and user data such as book title, author, read status, liked status, etc.
3. **Docker**: Ensures that both the Flask application and MySQL database can be run in isolated containers, making deployment simple and consistent.

## Setup and Installation

### Prerequisites
- Docker and Docker Compose installed on your local machine

### Running with Docker

1. Clone the repository:
   ```bash
    https://github.com/Laghrabi/Book_Shelf_API
    cd Book_Shelf_API
   ```

2. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. The API will be accessible at `http://localhost:5000`.

4. The MySQL database will run on `localhost:3306`.


## Testing

To test the application, you can use tools like **Postman** or **curl** to interact with the API endpoints. Ensure that the application is running either via Docker before testing.