from django.template import Library, Node


register = Library()

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 8
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 4

@register.inclusion_tag('paginator/paginator.html')
def paginator(page, url_format):
    num_pages = page.paginator.num_pages

    if (page.has_other_pages()):
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)

        if (num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = [n for n in range(1, num_pages + 1) if n > 0 and n <= num_pages]
        elif (page.number <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= num_pages]
            pages_outside_leading_range = [n + num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (page.number > num_pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, num_pages + 1) if n > 0 and n <= num_pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else:
            page_numbers = [n for n in range(page.number - ADJACENT_PAGES, page.number + ADJACENT_PAGES + 1) if n > 0 and n <= num_pages]
            pages_outside_leading_range = [n + num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        return {
            'url_format': url_format,
            'page': page,
            'page_numbers': page_numbers,
            'in_leading_range' : in_leading_range,
            'in_trailing_range' : in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'pages_outside_trailing_range': pages_outside_trailing_range,
        }

@register.simple_tag
def paginator_page_url(url_format, page):
    return url_format % (page,)
