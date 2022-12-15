from django import template

register = template.Library()


@register.simple_tag
def setvar(val=None):
    return val


@register.filter(name='debug_variable')
def debug(var):
    print(var)
    print(dir(var))
    print(type(var))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.filter
def remove_trailing(url):
    if url:
        if isinstance(url, str) and url.endswith("/"):
            return url[:-1]
    return url
