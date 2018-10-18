from django import template

register = template.Library()


@register.assignment_tag(name='sub_range')
def sub_range(page, difference):
    return range(max(page.paginator.num_pages - difference, 1),
                 min(page.paginator.num_pages + difference + 1, page.paginator.num_pages + 1))
