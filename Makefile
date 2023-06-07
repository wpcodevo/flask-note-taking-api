dev:
	docker-compose up -d

dev-down:
	docker-compose down

dev-down-v:
	docker-compose down -v

commands:
	mkdir flask-note-taking-api
	cd flask-note-taking-api 
	python3 -m venv venv
	# Migration
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade

install-modules:
	pip install flask flask-cors
	pip install flask_sqlalchemy python-dotenv psycopg2-binary
	pip install WTForms Flask-WTF
	pip install Flask-Migrate

start-server:
	flask run -p 8000 --reload

# start-server:
# 	python3 -m flask --app src/app run -p 8000 --reload 


