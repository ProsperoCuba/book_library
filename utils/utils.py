from django.contrib.sites.models import Site

from config.settings import SITE_ID


def get_current_site_no_request():
    """Returns active current site for no request actions"""
    return Site.objects.get(id=SITE_ID)
