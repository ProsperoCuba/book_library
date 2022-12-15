from django.db.models import F
from django.utils import timezone
from django.utils.timezone import now

from core.models import BookLoan


def get_current_date(use_time=False):
    """Return current date"""
    return timezone.now() if use_time else timezone.now().date()


def get_min_date():
    """
    Returns the min date for new book loan
    """
    today = now()
    return "{}-{}".format(today.year, today.strftime("%m-%d"))


def update_stock(books, less=None):
    """Method to update the in_stock field of the books."""
    update_kwargs = {"in_stock": F("in_stock") - 1 if less else F("in_stock") + 1}
    books.all().update(**update_kwargs)


def update_status():
    """Method to change the status of loans that have not been returned on the delivery date."""
    kwargs = {'status': 'past'}
    BookLoan.objects.filter(status='in_time').filter(end_date__lt=get_current_date()).update(**kwargs)
