from django import template
import random

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def index(list, index):
    return list[index]