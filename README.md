# Essentialis-API

This is a personal project of a RESTFul API relying on Python Flask framework and used to manage a small business of cosmetic products.

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
| PUT | /raw_materials| Updates a specific raw material entry in the database. | Content-type = application/JSON |
| DEL | /raw_materials | Removes a specific raw material entry from the database. | Content-type = application/JSON |

> Example of body (POST / PUT):
```json
{
  "description": "corante",
  "package_price": 30,
  "package_amt": 100,
  "unit_material": "mL"
}
```
> Example of body (DEL):
```json
{"description": "corante"}
```

| METHOD | Endpoint | Description | Header? |
| --- | --- | --- | --- |
| GET | /recipes| Returns all recipes stored in the database.  | N/A |
| POST | /recipe/<int:recipe_id> | Creates a new recipe entry in the database. | Content-type = application/JSON |
| PUT | /recipe | Updates a specific recipe entry in the database. | Content-type = application/JSON |
| DEL | /recipe | Removes a specific recipe entry from the database. | Content-type = application/JSON |

> Example of body (POST / PUT):
```json
{	
  "description": "Sabonete cheiroso",
  "labor_cost": 5,
  "supply_cost": 15
}
```
> Example of body (DEL):
```json
{"description": "Sabonete espetacular"}
```
