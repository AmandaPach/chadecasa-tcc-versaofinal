from django import template

register = template.Library()


@register.inclusion_tag("tags/status.html")
def status(is_active):
    if isinstance(is_active, str):
        is_active = is_active.lower() == "true"
    return {"active": bool(is_active)}
