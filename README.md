# **Test task for Insiders Software**

---

---

## **Dev**

Make sure you have [Poetry](https://python-poetry.org/) installed. To install all project dependencies, run:

```shell
poetry env use *the version of python you have installed ^3.13*
```

```shell
poetry install --no-root
```

Activate environment shell by:

```shell
poetry shell
```

---

## Run

Use next command to run project:

```shell
compose up --build -d
python manage.py runserver
```

---

## API Endpoints

### Authentication Endpoints

- **POST** `/api/v1/auth/register/`

  - Registers a new user.
  - **Request body**: User registration data (email, password, username)
  - **Response**: 201 Created or error message.

- **POST** `/api/v1/auth/password_reset/`

  - Requests a password reset link.
  - **Request body**: `{ "email": "user@example.com" }`
  - **Response**: 200 OK with a success message or error message.

- **POST** `/api/v1/auth/reset/<uidb64>/<token>/`
  - Confirms the password reset with the provided token and UID.
  - **Request body**: `{ "new_password": "new_password_value" }`
  - **Response**: 200 OK with a success message or error message.

### Locations Endpoints

- **GET** `/api/v1/locations/`

  - Lists all locations, with caching enabled for optimization.
  - **Response**: List of locations in JSON format.

- **GET** `/api/v1/locations/<id>/`

  - Retrieves detailed information about a specific location.
  - **Response**: Location details in JSON format.

- **POST** `/api/v1/locations/`

  - Creates a new location.
  - **Request body**: Location data (name, address)
  - **Response**: 201 Created with the location details.

- **PUT** `/api/v1/locations/<id>/`

  - Updates an existing location.
  - **Request body**: Updated location data.
  - **Response**: 200 OK with the updated location details.

- **DELETE** `/api/v1/locations/<id>/`

  - Deletes a specific location.
  - **Response**: 204 No Content.

- **GET** `/api/v1/locations/export/`
  - Exports the locations data in JSON or CSV format.
  - **Query Parameters**: `format=json` or `format=csv`
  - **Response**: A file download (CSV or JSON) containing the location data.

### Reviews Endpoints

- **GET** `/api/v1/locations/<location_pk>/reviews/`

  - Retrieves all reviews for a specific location.
  - **Response**: List of reviews for the location.

- **POST** `/api/v1/locations/<location_pk>/reviews/`

  - Creates a new review for a specific location.
  - **Request body**: Review data (e.g., comment, rating, etc.)
  - **Response**: 201 Created with the review details.

- **DELETE** `/api/v1/locations/<location_pk>/reviews/<id>/`
  - Deletes a specific review for a location.
  - **Response**: 204 No Content.

### Likes Endpoints

- **GET** `/api/v1/locations/<location_pk>/likes/`

  - Retrieves all likes for a specific location.
  - **Response**: List of likes for the location.

- **POST** `/api/v1/locations/<location_pk>/likes/`

  - Creates a like for a specific location.
  - **Request body**: Like data (e.g., is_like=True/False).
  - **Response**: 201 Created with the like details.

- **DELETE** `/api/v1/locations/<location_pk>/likes/<id>/`
  - Deletes a specific like for a location.
  - **Response**: 204 No Content.

---

## Author

### Mykhailo Rozhkov

[LinkedIn](https://www.linkedin.com/in/mykhailo-rozhkov/)  
[Telegram](https://t.me/datrevter)  
Email: rozhkovm176@gmail.com
