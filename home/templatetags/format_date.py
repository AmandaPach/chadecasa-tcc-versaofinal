from django import template
import re

register = template.Library()

formated_pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
javascript_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

@register.filter
def format_date(date_str):
    if date_str.endswith("-03:00"):
        date_str = date_str[:-6]

    if formated_pattern.match(date_str):
        date = date_str.split(" ")[0]
        ano, mes, dia = date.split("-")
        return f"{dia}/{mes}/{ano}"

    if javascript_pattern.match(date_str):
        date, _ = date_str.split("T")
        ano, mes, dia = date.split("-")
        return f"{dia}/{mes}/{ano}"
    
    return date_str
