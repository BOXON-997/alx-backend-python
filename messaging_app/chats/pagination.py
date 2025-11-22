# pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Pagination for messages.
    Fetches 20 messages per page.
    """
    page_size = 20
    page_query_param = "page"
