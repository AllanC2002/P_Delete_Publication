# Delete Publication Microservice

This project is a Python-based backend service built with Flask. It provides an API endpoint for managing publications, specifically for marking publications as deleted (soft delete). The service interacts with a MongoDB database.

## Folder Structure

The project follows a layer-based folder organization:

-   **`.github/workflows/`**: Contains CI/CD pipeline configurations for GitHub Actions, used for building and publishing Docker images for different environments (e.g., `docker-publish.yml`, `docker-publish_qa.yml`).
-   **`conections/`**: Manages database connectivity.
    -   `mongo.py`: Contains the logic to connect to the MongoDB database.
-   **`services/`**: Contains the business logic of the application.
    -   `functions.py`: Implements core functionalities, such as deleting a publication.
-   **`tests/`**: Includes test scripts for the application.
    -   `route_test.py`: An integration test for the API endpoints.
    -   `test_delete_publication.py`: (Presumably) Unit tests for the delete publication functionality.
-   **`main.py`**: The main entry point for the Flask application. It defines API routes, handles incoming requests, and orchestrates calls to the service layer.
-   **`dockerfile`**: Instructions for building a Docker image of the application.
-   **`requirements.txt`**: Lists the Python dependencies required for the project.
-   **`.gitignore`**: Specifies files and directories to be ignored by Git.
-   **`__pycache__/`**: (Typically in .gitignore) Directories containing Python bytecode, automatically generated.

## Backend Design Pattern

The application primarily uses a **Layered Architecture**. This pattern separates concerns into distinct layers:

1.  **Presentation Layer (API Layer)**: Implemented in `main.py` using Flask. This layer is responsible for handling HTTP requests, authentication, request/response formatting (JSON), and routing requests to the service layer.
2.  **Service Layer (Business Logic Layer)**: Implemented in `services/functions.py`. This layer contains the core application logic and orchestrates data operations by interacting with the data access layer.
3.  **Data Access Layer (Persistence Layer)**: Implemented in `conections/mongo.py`. This layer is responsible for all database interactions, abstracting the database operations from the service layer.

## Communication Architecture

-   **External Communication**: Clients interact with the service via **HTTP/HTTPS** requests to the API endpoints defined in `main.py` (Flask).
-   **Internal Communication**:
    -   The API Layer (`main.py`) communicates with the Service Layer (`services/functions.py`) through direct **Python function calls**.
    -   The Service Layer (`services/functions.py`) communicates with the Data Access Layer (`conections/mongo.py`) also through direct **Python function calls**.

## API Endpoint Instructions

### `PUT /delete-publication`

Marks a publication as deleted by setting its `Status` field to `0` in the database (soft delete).

-   **HTTP Method**: `PUT`
-   **URL Path**: `/delete-publication`
-   **Headers**:
    -   `Authorization`: `Bearer <JWT_TOKEN>` (Required)
        -   The JWT token is expected to contain a `user_id` in its payload.
-   **Request Body**:
    -   Content-Type: `application/json`
    -   **Schema**:
        ```json
        {
          "publication_id": "string" // The MongoDB ObjectId of the publication to delete.
        }
        ```
    -   **Example**:
        ```json
        {
          "publication_id": "686878a7de34f79af1d73029"
        }
        ```

-   **Success Responses**:
    -   **`200 OK`**: Indicates the publication was successfully marked as deleted.
        -   **Body**:
            ```json
            {
              "message": "Publication deleted successfully"
            }
            ```

-   **Error Responses**:
    -   **`400 Bad Request`**:
        -   If `publication_id` is missing from the request body.
            ```json
            {
              "error": "publication_id is required"
            }
            ```
        -   If `publication_id` is not a valid MongoDB ObjectId format.
            ```json
            {
              "error": "Invalid ObjectId format"
            }
            ```
    -   **`401 Unauthorized`**:
        -   Token missing or invalid format (not "Bearer <token>").
            ```json
            {
              "error": "Token missing or invalid"
            }
            ```
        -   Token has expired.
            ```json
            {
              "error": "Token expired"
            }
            ```
        -   Token is invalid (e.g., signature verification failed, malformed).
            ```json
            {
              "error": "Invalid token"
            }
            ```
        -   Token is valid but does not contain the required `user_id`.
            ```json
            {
              "error": "Invalid token data"
            }
            ```
    -   **`404 Not Found`**:
        -   If no publication matches the provided `publication_id`.
            ```json
            {
              "error": "Publication not found"
            }
            ```
    -   **`500 Internal Server Error`**:
        -   For any other unexpected errors on the server.
            ```json
            {
              "error": "Internal server error: <specific_error_details>"
            }
            ```
