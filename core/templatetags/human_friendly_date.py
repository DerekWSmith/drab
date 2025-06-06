from django import template

register = template.Library()

@register.filter
def human_friendly_date(value):
    if not value:
        return ''
    return value.strftime('%d-%b-%y %H:%M:%S')