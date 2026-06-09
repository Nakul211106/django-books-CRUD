import csv
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = "Import books from the Kaggle CSV dataset"

    def handle(self, *args, **options):
        csv_path = (
            Path(settings.BASE_DIR)
            / "Books_Data_Clean-selected-columns.csv"
        )

        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"CSV file not found: {csv_path}"
                )
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with csv_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                try:
                    kaggle_index = int(row["index"])

                    publishing_year = self.parse_year(
                        row["Publishing Year"]
                    )

                    book_name = self.clean_text(
                        row["Book Name"],
                        default=f"Unknown Book {kaggle_index}",
                    )

                    author = self.clean_text(
                        row["Author"],
                        default="Unknown Author",
                    )

                    language_code = self.clean_text(
                        row["language_code"],
                        default="Unknown",
                    )

                    author_rating = self.clean_text(
                        row["Author_Rating"],
                        default="Novice",
                    )

                    book_average_rating = float(
                        row["Book_average_rating"]
                    )

                    book_ratings_count = int(
                        float(row["Book_ratings_count"])
                    )

                    genre = self.clean_text(
                        row["genre"],
                        default="Unknown",
                    )

                    gross_sales = self.parse_decimal(
                        row["gross sales"]
                    )

                    book, created = Book.objects.update_or_create(
                        kaggle_index=kaggle_index,
                        defaults={
                            "publishing_year": publishing_year,
                            "book_name": book_name,
                            "author": author,
                            "language_code": language_code,
                            "author_rating": author_rating,
                            "book_average_rating": (
                                book_average_rating
                            ),
                            "book_ratings_count": (
                                book_ratings_count
                            ),
                            "genre": genre,
                            "gross_sales": gross_sales,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except (
                    KeyError,
                    TypeError,
                    ValueError,
                    InvalidOperation,
                ) as error:
                    skipped_count += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped CSV row {row_number}: {error}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Import completed\n"
                f"Created: {created_count}\n"
                f"Updated: {updated_count}\n"
                f"Skipped: {skipped_count}"
            )
        )

    def clean_text(self, value, default):
        if value is None:
            return default

        value = value.strip()

        if value == "" or value.lower() == "nan":
            return default

        return value

    def parse_year(self, value):
        if value is None:
            return None

        value = value.strip()

        if value == "" or value.lower() == "nan":
            return None

        number = float(value)

        if math.isnan(number):
            return None

        return int(number)

    def parse_decimal(self, value):
        if value is None:
            return Decimal("0.00")

        value = value.strip()

        if value == "" or value.lower() == "nan":
            return Decimal("0.00")

        return Decimal(value).quantize(Decimal("0.01"))