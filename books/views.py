from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book


def book_list(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    author_rating = request.GET.get("author_rating", "").strip()

    books = Book.objects.all().order_by("kaggle_index")

    if query:
        books = books.filter(
            Q(book_name__icontains=query)
            | Q(author__icontains=query)
            | Q(language_code__icontains=query)
        )

    if genre:
        books = books.filter(genre__iexact=genre)

    if author_rating:
        books = books.filter(author_rating=author_rating)

    genres = (
        Book.objects.values_list("genre", flat=True)
        .distinct()
        .order_by("genre")
    )

    context = {
        "books": books,
        "query": query,
        "selected_genre": genre,
        "selected_author_rating": author_rating,
        "genres": genres,
        "author_rating_choices": Book.AUTHOR_RATING_CHOICES,
    }

    return render(request, "books/book_list.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    return render(
        request,
        "books/book_detail.html",
        {"book": book},
    )


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        next_index = (
            Book.objects.order_by("-kaggle_index")
            .values_list("kaggle_index", flat=True)
            .first()
        )

        if next_index is None:
            next_index = 0
        else:
            next_index += 1

        form = BookForm(initial={"kaggle_index": next_index})

    return render(
        request,
        "books/book_form.html",
        {
            "form": form,
            "heading": "Add Book",
            "button_text": "Add Book",
        },
    )


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            book = form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "books/book_form.html",
        {
            "form": form,
            "heading": "Update Book",
            "button_text": "Save Changes",
        },
    )


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(
        request,
        "books/book_confirm_delete.html",
        {"book": book},
    )