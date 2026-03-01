from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split the string by the given argument"""
    if value:
        return value.split(arg)
    return []

@register.filter
def last(value):
    """Get last item of a list"""
    if value and len(value) > 0:
        return value[-1]
    return ''

@register.filter
def slice(value, arg):
    """Slice a string"""
    if value:
        try:
            return value[:int(arg)]
        except:
            return value
    return ''