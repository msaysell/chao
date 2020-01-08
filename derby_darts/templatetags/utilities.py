from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag(name='sub_range')
def sub_range(page, difference):
    return range(max(page.paginator.num_pages - difference, 1),
                 min(page.paginator.num_pages + difference + 1, page.paginator.num_pages + 1))

def parse_date_string(date):
    if date is not None:
        return datetime.fromisoformat(date.rstrip("Z"))
register.filter('parse_date_string', parse_date_string)
