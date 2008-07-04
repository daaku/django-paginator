from django.template import Library, Node


register = Library()

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 8
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 4

@register.inclusion_tag('paginator/paginator.html', takes_context=True)
def paginator(context):
    paginator = context['paginator']
    page = context['jewelry']
    current_page_number = page.number

    if (page.has_other_pages()):
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)

        if (paginator.num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = [n for n in range(1, paginator.num_pages + 1) if n > 0 and n <= paginator.num_pages]
        elif (current_page_number <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= paginator.num_pages]
            pages_outside_leading_range = [n + paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (current_page_number > paginator.num_pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(paginator.num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, paginator.num_pages + 1) if n > 0 and n <= paginator.num_pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else:
            page_numbers = [n for n in range(current_page_number - ADJACENT_PAGES, current_page_number + ADJACENT_PAGES + 1) if n > 0 and n <= paginator.num_pages]
            pages_outside_leading_range = [n + paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        return {
            'base_url': 'blah?page=', #FIXME
            'is_paginated': page.has_other_pages(),
            'previous': page.previous_page_number(),
            'has_previous': page.has_previous(),
            'next': page.next_page_number(),
            'has_next': page.has_next(),
            'results_per_page': 6, #FIXME
            'current_page_number': current_page_number,
            'pages': paginator.num_pages,
            'page_numbers': page_numbers,
            'in_leading_range' : in_leading_range,
            'in_trailing_range' : in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'pages_outside_trailing_range': pages_outside_trailing_range
        }
