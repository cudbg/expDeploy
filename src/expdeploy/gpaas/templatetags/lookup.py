from django import template
register = template.Library()
import socket

@register.simple_tag
def lookup(dictionary, key):
	uuid_filename = dictionary.get (key,'')
	return dictionary.get(uuid_filename, '')

@register.simple_tag
def explink(dictionary, key):
	return dictionary.get(key)

@register.simple_tag
def expfullink(dictionary, key):
	return "https://192.241.179.74:8001" + dictionary.get(key)