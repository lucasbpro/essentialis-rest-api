# Essentialis-API

This is a personal project of a RESTFul API used to manage a small business of cosmetic products.

## How to run the API server

The API is started by running the commands below in a Bash or in the
command prompt. They create a virtual environment, install all project dependencies on it and then run the application.

For Linux/MAC:
```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python app.py
```
For Windows:
```bash
virtualenv venv
. venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

## API Endpoints

| METHOD | Endpoint | Description | Header? |
| --- | --- | --- | --- |
| GET | /raw_materials| Returns all raw materias stored in the database.  | N/A |
| POST | /raw_materials| Creates a new raw material entry in the database. | N/A |
| PUT | /raw_materials| Updates a specific raw material entry in the database. | Content-type = application/JSON
