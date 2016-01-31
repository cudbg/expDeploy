from django import template
register = template.Library()

@register.simple_tag
def lookup(dictionary, key):
    return dictionary.get(key, '')
