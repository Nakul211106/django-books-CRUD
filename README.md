# Django Kaggle Books CRUD Application

A Django-based Book Sales and Ratings Management System built using a Kaggle CSV dataset.

## Features

- Import book records from a Kaggle CSV dataset
- Display all books
- Search and filter books
- View individual book details
- Add new books
- Update book information
- Delete books
- Export updated database records to CSV
- Manage records through Django Admin

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Kaggle CSV dataset

## Dataset Fields

- Index
- Publishing Year
- Book Name
- Author
- Language Code
- Author Rating
- Book Average Rating
- Book Ratings Count
- Genre
- Gross Sales

## Project Structure

```text
django-books-CRUD/
├── manage.py
├── requirements.txt
├── Books_Data_Clean-selected-columns.csv
├── books/
│   ├── management/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── mysite/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py