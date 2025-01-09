# Django Project with Language Model

This is a Django-based project that integrates a language model for question-answering functionality.

## Features

- **Language Model Integration**: Supports semantic search and question answering using a pre-trained language model.
- **Database-Driven Knowledge Base**: Questions and answers are stored in a database for efficient retrieval.
- **Admin Panel**: Manage questions and answers via Django's admin interface.

## Requirements

- Python 3.8+
- Django 4.0+
- SQLite3 (default database)
- sentence-transformers

## Create a virtual environment:

python -m venv venv \
bash: venv\Scripts\activate


## Install dependencies

pip install -r requirements.txt

## Apply migrations

python manage.py migrate

## Run Server
python manage.py runserver

## Safety

Create file secret.py with parameter Secret = <YOUR_DJANGO_SECRET_KEY>

import file to the settings.py

SECRET_KEY = Secret


