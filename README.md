# BookselfAPI v3.1-beta.1 📖

[![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://cryptic-river-21647-7efe93940f14.herokuapp.com/api_v3)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

[![License: MIT](https://img.shields.io/github/license/yo1am1/bookstoreAPI)](https://github.com/yo1am1/bookstoreAPI/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/yo1am1/bookstoreAPI)](https://github.com/yo1am1/bookstoreAPI/commits/main)
[![codecov](https://codecov.io/gh/yo1am1/BookselfAPI/branch/main/graph/badge.svg?token=erUjdAbB6E)](https://app.codecov.io/gh/yo1am1/BookselfAPI)
![Lint](https://github.com/yo1am1/bookstoreAPI/actions/workflows/black.yaml/badge.svg?event=push)
![Pytest](https://github.com/yo1am1/bookstoreAPI/actions/workflows/test.yml/badge.svg?event=push)
![GitHub Latest Pre-Release)](https://img.shields.io/github/v/release/yo1am1/bookstoreAPI?include_prereleases&label=pre-release&logo=github)

[![Documentation](https://img.shields.io/badge/API%20Documentation-Explore%20Here-blue)](https://app.swaggerhub.com/apis-docs/BIGDIEBAM/book-shelf_social_experiment/3.1-beta.1)

[![Swagger Validator](https://validator.swagger.io/validator?url=https://raw.githubusercontent.com/yo1am1/bookstoreAPI/main/swagger.yml)](https://app.swaggerhub.com/apis-docs/BIGDIEBAM/book-shelf_social_experiment/3.1-beta.1)
    
## Table of Contents 📚:

- [Introduction](#bookselfapi-v31-beta1-)
- [Key Features](#key-features-)
- [Installation and Usage](#installation-and-usage-)
- [Contributing](#contributing-️)
- [Security](#security-)
- [License](#license-️)

## Introduction

Welcome to BookselfAPI, your digital bookshelf project. This repository contains the backend API for managing your book collection.

## Key Features 🔑

- [API Documentation](https://app.swaggerhub.com/apis-docs/BIGDIEBAM/book-shelf_social_experiment/3.1-beta.1): Explore the endpoints, methods, and functionalities provided by the API using Swagger.
> [!NOTE]\
> Although, you can find documentation in [swagger.yml](https://github.com/yo1am1/bookstore-api/blob/bookselfAPI/swagger.yml) file.

## Installation and Usage 🧠

1. Clone the repository:
    ```bash
    git clone https://github.com/yo1am1/bookselfAPI.git
    ```

2. Navigate to the project directory and either open it in PyCharm or use the terminal.

3. Migrate changes:
    ```bash
    python manage.py migrate
    ```
    
4. Run API on local server.
    ```bash
    python manage.py runserver
    ```
    
    > [!IMPORTANT]\
    > You can specify port at the end of this command, if you do not want to use default port

5. Access the API at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

    > [!NOTE]\
    > Or at the port you specified before. For example: [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

6. Enjoy managing your digital bookshelf!

## Contributing 🗺️

If you'd like to contribute to the project, please read the [Contributing Guidelines](CONTRIBUTING.md) for more information.

## Security 👮

For information on security practices and how to report vulnerabilities, please read our [Security Policy](SECURITY.md).

## License ⛓️

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Thank you for using BookselfAPI. We hope it enhances your book management experience!
