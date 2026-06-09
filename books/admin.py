from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "kaggle_index",
        "book_name",
        "author",
        "publishing_year",
        "author_rating",
        "book_average_rating",
        "genre",
        "gross_sales",
    ]

    search_fields = [
        "book_name",
        "author",
        "language_code",
        "genre",
    ]

    list_filter = [
        "author_rating",
        "genre",
        "language_code",
    ]

    ordering = ["kaggle_index"]