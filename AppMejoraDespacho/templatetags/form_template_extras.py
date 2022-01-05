from django import template

register = template.Library()

@register.filter
def get_region(dictionary, key):
    return dictionary[key-1][1]

@register.filter
def get_comunas_por_region(dictionary, key):
    return dictionary[key-1]

@register.filter
def get_comuna(dictionary, key):
    return dictionary[int(key)-1][1]