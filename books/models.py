from django.db import models


class Book(models.Model):
    AUTHOR_RATING_CHOICES = [
        ("Novice", "Novice"),
        ("Intermediate", "Intermediate"),
        ("Excellent", "Excellent"),
        ("Famous", "Famous"),
    ]

    kaggle_index = models.IntegerField(unique=True)
    publishing_year = models.IntegerField(null=True, blank=True)
    book_name = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    language_code = models.CharField(
        max_length=20,
        blank=True,
        default="Unknown",
    )
    author_rating = models.CharField(
        max_length=20,
        choices=AUTHOR_RATING_CHOICES,
    )
    book_average_rating = models.FloatField()
    book_ratings_count = models.IntegerField()
    genre = models.CharField(max_length=100)
    gross_sales = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    def __str__(self):
        return self.book_name