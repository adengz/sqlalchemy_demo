# sqlalchemy_demo
SQLAlchemy ORM demo with Flask-SQLAlchemy

## Enviornment setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start server
```
python app.py
```

## Testing API with Postman
With server running, import `flask-sqlalchemy-demo.postman_collection.json` into Postman and have fun with it. Note none of the calls are idempotent, but you can always start fresh by restarting the server.