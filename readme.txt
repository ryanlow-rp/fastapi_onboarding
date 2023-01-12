Instructions for Varys backend
==============================
git clone https://ygitlab.southeastasia.cloudapp.azure.com/youzu_ai/new-varys/backend-service
make migrate
docker-compose up -d --build


docker stop backend-service-pg_admin-1
docker stop varys-backend
docker stop backend-service-db-1
docker stop varys-proxy
docker container prune


docker-compose exec web pytest /usr/src/app/tests/test_main.py
docker-compose exec web pytest tests/unit/.
docker-compose exec web pytest tests/functional/.


venv
====
python3 -m pip install --user virtualenv
virtualenv venv
source venv/bin/activate

tutorial
========
https://testdriven.io/blog/fastapi-crud/

onboarding
==========
https://youzu.feishu.cn/docx/HIR7dJBX4ourpXxtIkmcbmQVnNc

pip install
===========
python3 -m pip install --user black

black usage
===========
python3 -m black ./src

list all files
==============
find . | grep .py

Start docker containers
=======================
docker-compose up -d --build

Run tests
=======================
docker-compose exec web pytest .

Stop docker containers
======================
docker stop onboarding-web-1
docker stop onboarding-db-1
docker stop onboarding-caddy-1
docker stop onboarding-pg_admin-1
docker container prune

Connect to database in docker
=============================

docker-compose exec db psql --username=onboarding --dbname=onboarding_dev

When inside database in docker
==============================

\l
\c onboarding_dev
\dt
\d artifacts
\q

View console output from docker
===============================
docker logs onboarding-web-1

URL
===
http://localhost:8000
http://localhost:8000/docs

http://localhost:8000/api/v1/
http://localhost:8000/api/v1/docs

Testing unique field in table
=============================
https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-unique-constraint/
https://dev.to/rexosei/how-to-make-a-field-unique-with-sqlmodel-4km9

CREATE TABLE person (
	id SERIAL  PRIMARY KEY,
	first_name VARCHAR (50),
	last_name  VARCHAR (50),
	email      VARCHAR (50),
        UNIQUE(email)
);

INSERT INTO person(first_name,last_name,email)
VALUES('john','doe','j.doe@postgresqltutorial.com');

INSERT INTO person(first_name,last_name,email)
VALUES('jack','doe','j.doe@postgresqltutorial.com');

