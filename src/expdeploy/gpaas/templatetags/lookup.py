from django import template
register = template.Library()
import socket

@register.filter
def is_published(dictionary,value): # Only one argument.
    """Converts a string into all lowercase"""
    console.log(dictionary)
    return True

@register.simple_tag
def lookup(dictionary, key):
	uuid_filename = dictionary.get (key,'')
	return dictionary.get(uuid_filename, '')

@register.simple_tag
def explink(dictionary, key):
	return dictionary.get(key)

@register.simple_tag
def expfullink(dictionary, key):
	return "https://gpaas.xyz" + str(dictionary.get(key))