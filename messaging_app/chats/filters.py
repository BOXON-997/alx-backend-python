import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages:
    - by user (sender)
    - by date range (timestamp)
    """
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr="iexact")
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']

