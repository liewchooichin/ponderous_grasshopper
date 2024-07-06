# home/page_util.py

# paginator, page number checking utilities

# Shared function to get the query parameter that
# stores the number of items to display on the page.
# Allow at most 20 items per page.
def _get_items_per_page(request):
    """Determine how many items to show
       per page.
    """
    # Set default items_per_page to 10
    max_items_per_page = 20
    default_items_per_page = 10
    items_per_page = \
        int(request.GET.get('items_per_page', default_items_per_page))
    if items_per_page < 1:
        items_per_page = default_items_per_page
    if items_per_page > max_items_per_page:
        items_per_page = max_items_per_page

    return items_per_page

# Shared function to get the query parameter that stores
# the page number to be displayed
def _get_page_num(request, paginator):
    """Get current page number for pagination,
    using reasonable defaults."""
    page_num = int(request.GET.get("page", 1))
    if page_num < 1: 
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages
    
    return page_num

