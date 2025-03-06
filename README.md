[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
![size-shield]
![commit-shield]

<p align="center">
  <h1 align="center">📄 Management Blog</h1>

  <p align="center">
    <img src="https://github.com/viniciusperrone/management-blog/blob/master/static/management_blog_diagram.png" alt="Logo" heigth="200px">
  </p>
</p>

## Table of Contents

* [About the Project](#about-the-project)
* [How to install?](#how-to-install)
* [Built With](#built-with)

## About the Project

Management Blog is a system that allows users to register, edit and delete articles, as well as rate published content.

It has the following features:

- User registration
- Authentication system
- Category registration
- Registering/Updating/Deleting articles
- List of articles
- Search for articles by any data provided

<p align="center">
    <img src="https://github.com/viniciusperrone/management-blog/blob/master/static/management_blog_gif.gif" alt="Logo" height="200px">
</p>

## How to install?

Running the project on your machine is a simple process. Make sure you have Docker Engine or Docker Desktop installed on your machine. Then update the environment variables in the .env file, as follows: 

```env
SQLALCHEMY_DATABASE_URI=
SQLALCHEMY_TRACK_MODIFICATIONS=
SQLALCHEMY_ECHO=

JWT_SECRET_KEY=

ELASTICSEARCH_URL=
ELASTICSEARCH_USER=
ELASTICSEARCH_PASSWORD=
```

After that, start all the services declared in the docker-compose file. To do this, run the following command.

```bash
$ docker-compose up -d --build
```

With the containers running, we need to migrate their models to our postgres database. To do this, run the following commands:

```bash
$ docker exec -it blog-api /bin/bash

root@274c42373ef1:/app# flask db migrate

root@274c42373ef1:/app# flask db upgrade
```

Now our application is running. If you want to test it, run the following commands:

```bash
$ docker exec -it blog-api /bin/bash

root@274c42373ef1:/app# export TESTING=True

root@274c42373ef1:/app# pytest
```

## Built With

* Backend Framework: [Flask](https://flask.palletsprojects.com/)
* Database technology: [Postgres](https://www.postgresql.org/), [Elasticsearch](https://www.elastic.co/pt/elasticsearch), and [SQLite](https://www.sqlite.org/)
* Backend data processing technology: [SQLALchemy](https://docs.sqlalchemy.org/)
* Technology for testing implementation: [Pytest](https://docs.pytest.org/en/stable/)
* API documentation tool: [SwaggerHUB](https://swagger.io/tools/swaggerhub/)
* Diagram creation tool: [dbdiagram.io](https://dbdiagram.io/)

[contributors-shield]: https://img.shields.io/github/contributors/viniciusperrone/management-blog?style=flat-square
[contributors-url]: https://github.com/viniciusperrone/management-blog/graphs/contributors

[issues-shield]: https://img.shields.io/github/issues/viniciusperrone/management-blog?style=flat-square
[issues-url]: https://github.com/viniciusperrone/management-blog/issues

[size-shield]: https://img.shields.io/github/repo-size/viniciusperrone/management-blog?style=flat-square

[commit-shield]: https://img.shields.io/github/last-commit/viniciusperrone/management-blog?style=flat-square
