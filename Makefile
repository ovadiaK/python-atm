make tests:
	pytest server/test_server.py

make run:
	FLASK_APP=server/app.py flask run