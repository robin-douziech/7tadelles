from django import template
import random
from datetime import datetime

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def index(list, index):
    return list[index]

@register.filter
def week_day(date) :
    day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    return day_names[date.weekday()]

@register.filter
def month_str(date) :
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    return month_names[date.month-1]

@register.filter
def get_dict_value(dic, key) :
    return dic[key]