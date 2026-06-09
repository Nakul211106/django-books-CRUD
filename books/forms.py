from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "kaggle_index",
            "publishing_year",
            "book_name",
            "author",
            "language_code",
            "author_rating",
            "book_average_rating",
            "book_ratings_count",
            "genre",
            "gross_sales",
        ]

        widgets = {
            "kaggle_index": forms.NumberInput(
                attrs={"placeholder": "Dataset index"}
            ),
            "publishing_year": forms.NumberInput(
                attrs={"placeholder": "Publishing year"}
            ),
            "book_name": forms.TextInput(
                attrs={"placeholder": "Book name"}
            ),
            "author": forms.TextInput(
                attrs={"placeholder": "Author name"}
            ),
            "language_code": forms.TextInput(
                attrs={"placeholder": "Example: eng or en-US"}
            ),
            "book_average_rating": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "max": "5",
                }
            ),
            "book_ratings_count": forms.NumberInput(
                attrs={"min": "0"}
            ),
            "genre": forms.TextInput(
                attrs={"placeholder": "Book genre"}
            ),
            "gross_sales": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }

    def clean_book_average_rating(self):
        rating = self.cleaned_data["book_average_rating"]

        if rating < 0 or rating > 5:
            raise forms.ValidationError(
                "Book rating must be between 0 and 5."
            )

        return rating