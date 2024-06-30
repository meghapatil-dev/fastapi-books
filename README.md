## FASTAPI - Books

# Setup
1. Create python virtual enviornment
```sh
python -m venv .env
```

2. Install all the dependencies from `requirements.txt`
```sh
python -m pip install -r requirements.txt
```

3. Activate venv
```sh
Source .env/Scripts/activate
```

4. Run FastAPI app
```sh
uvicorn main:app --reload
```

5. Run test cases
```sh
pytest test_main.py
```

## Database Schema
Refer Database schema here :  [Books DB](./books_sql.sql)

## Documention 

Refer swagger document here : [API DOCS](./openapi.json)

