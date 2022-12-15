from django.contrib.sites.shortcuts import get_current_site


def global_variables(request):
    """
    Return context global variables for use in templates.
    """
    context_extras = dict()

    context_extras['current_site'] = get_current_site(request)

    return context_extras
