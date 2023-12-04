# KiddoQuest

Parenting Apps to tracking student classes.


## File Structure
1. **config.py:** Application configuration file, including database connections and environment variables.
2. **crud.py:** CRUD module containing functions for entities such as students, classes, instructors, and student interests.
3. **dockerfile:** Dockerfile definition for running the application as a Docker container.
4. **main.py:** Main file serving as the entry point for FastAPI execution, including database table creation if not existing.
5. **models.py:** Models module with entity (model) definitions such as Student, Class, Instructor, and StudentInterest.
6. **requirements.txt:** File listing Python packages required by the application.
7. **routes.py:** Routes module containing API endpoint definitions and CRUD operations logic.
8. **schemas.py:** Schemas module with data schema definitions for API request and response validation.

## Routes
- **POST /token (Generate Token):**
  - Generates a JWT token based on the provided username and password.
  - Uses the `generate_token` function in the authentication module.

- **POST /users (Create User):**
  - Creates a new user with a username and password.
  - Uses the `create_user` function in the authentication module.

- **GET /users/me (Get Current User):**
  - Retrieves information about the current user (ID, username, and role).
  - Uses the `get_user` function in the authentication module.

- **GET /students/ (Get Students):**
  - Retrieves a list of students from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_students` to retrieve student data.

- **GET /classes/ (Get Classes):**
  - Retrieves a list of classes from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_classes` to retrieve class data.

- **GET /instructors/ (Get Instructors):**
  - Retrieves a list of instructors from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_instructors` to retrieve instructor data.

## How to Run
1. Clone this repository.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Run the application with the command `uvicorn main:app --reload`.

## How to Test
1. Open Swagger Documentation to view and test API endpoints.
2. Use the `/token` endpoint to generate a token by sending a username and password via Form Data.
3. Use the generated token to access the `/users/me` endpoint to get information about the current user.

## Docker Deployment
1. Build the Docker image with the command `docker build -t marilearn-auth-service ..`.
2. Run the Docker container with the command `docker run -p 80:80 marilearn-auth-service`.
