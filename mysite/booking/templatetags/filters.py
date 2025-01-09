from django import template
from ..models import CITIES

register = template.Library()

@register.filter
def to_euros(cts):
    return cts/100

@register.filter
def to_full_name(city):
    return CITIES.get(city)