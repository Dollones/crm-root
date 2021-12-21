from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django_filters.views import FilterView
from .models import Client
from .const import INDEX_PAGINATE_BY
from .filters import ClientFilter


class CompanyListView(FilterView):
    queryset = Client.objects.all()
    template_name = 'cms_mainpage/list_page.html'
    paginate_by = INDEX_PAGINATE_BY
    filterset_class = ClientFilter


