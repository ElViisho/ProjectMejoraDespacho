from django import template

register = template.Library()

@register.filter
def get_comuna(dictionary, key):
    return dictionary[key][1]