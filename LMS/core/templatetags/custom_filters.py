from django import template
from core.models import Book, BookReturn

register = template.Library()

@register.filter
def exclude_returned_books(approved_books, returned_books):
    return [book for book in approved_books if book not in returned_books]
