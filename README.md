# python-atm
a money machine written with TDD in python


## running the tests
```commandline
pytest tests/test_server.py
```

### behavior file
under `features/atm_server.feature` a behavior file can be found documenting the server behavior

## running the server
```commandline
export FLASK_APP=atm_server/app.py
flask run
```
### refilling

`POST /refill` endpoint accepts a json in the following format:
```json
{
  "bills": {
    "200": 7,
    "100": 4,
    "20": 15
  },
  "coins": {
    "10": 10,
    "5": 1,
    "1": 10,
    "0.1": 12,
    "0.01": 21
  }
}
```
example
```commandline
curl -X POST  http://127.0.0.1:5000/refill -H 'Content-Type: application/json'  -d '{"bills": {"200": 7}, "coins": {}}'
```

### withdrawal

`POST /withdrawal` endpoint accepts a json in the following format:
```json
{"amount": 12.3}
```
example
```commandline
curl -X POST  http://127.0.0.1:5000/withdrawal -H 'Content-Type: application/json'  -d '{"amount": 12.3}'
```

