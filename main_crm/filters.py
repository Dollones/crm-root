import django_filters as filters
from django.utils.translation import gettext_lazy as _

from main_crm.models import Client


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = _('%s (Обратно)')


class ClientFilter(filters.FilterSet):
    sort_by = MyOrderingFilter(
        fields=('company_name', 'published'),
        field_labels={
            'published': 'Дата публикации',
            'company_name': 'Названию компании'
        }
    )

    class Meta:
        model = Client
        fields = ['sort_by']
