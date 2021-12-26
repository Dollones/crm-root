import django_filters as filters
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from main_crm.models import Company, Interaction


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = _('%s (Обратно)')


class CompanyFilter(filters.FilterSet):
    sort_by = MyOrderingFilter(
        fields=('company_name', 'published'),
        field_labels={
            'published': 'Дата публикации',
            'company_name': 'Названию компании'
        }
    )

    class Meta:
        model = Company
        fields = ['sort_by']


class InteractionFilter(filters.FilterSet):
    project__icontains = filters.CharFilter(label='Поиск по проекту', field_name='project__title',
                                            lookup_expr='icontains')
    company__icontains = filters.CharFilter(label='Поиск по компании', field_name='project__user__company_name',
                                            lookup_expr='icontains')
    manager = filters.ModelChoiceFilter(queryset=User.objects.filter(is_superuser=True))

    class Meta:
        model = Interaction
        fields = ['channel', 'manager', 'mark']
