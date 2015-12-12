"""
TemplateTags to use the enums in template
"""
from django import template
from cooking.references.Enums import INGREDIENT_TYPES,MEASUREMENT
from django.utils.translation import ugettext as _

register = template.Library()


def get_measurements() :
    return dict((key,_(value)) for (key,value) in MEASUREMENT)


def get_ingredients_types() :
    return dict( (key,_(value)) for (key,value) in INGREDIENT_TYPES)

@register.filter
def get_measure(raw_value):
    return [ _(me[1]) for me in MEASUREMENT if me[0] == raw_value][0]

@register.filter
def get_ingredient_type(raw_value):
    return [ _(ig[1]) for ig in INGREDIENT_TYPES if ig[0] == raw_value][0]