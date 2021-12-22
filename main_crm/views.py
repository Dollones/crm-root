from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import CompanyForm
from .models import Company
from .const import INDEX_PAGINATE_BY
from .filters import CompanyFilter
from .utils import slugify


class CompanyListView(FilterView):
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/list_page.html'
    paginate_by = INDEX_PAGINATE_BY
    filterset_class = CompanyFilter

    def get_context_data(self, *args, **kwargs):
        sort_by = self.request.GET.get('sort_by', '')
        sort_by_param = f'&sort_by={sort_by}'
        return super().get_context_data(*args, sort_by_param=sort_by_param, **kwargs)


class CompanyDetialView(DetailView):
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/detail_page.html'
    slug_url_kwarg = 'company_slug'


class CompanyCreateView(CreateView):
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/create_company.html'
    form_class = CompanyForm

    def form_valid(self, form):
        cd = form.cleaned_data
        cd['slug'] = slugify(cd['company_name'])
        self.object = Company.objects.create(**cd)
        return HttpResponseRedirect(self.get_success_url())


class CompanyUpdate(UpdateView):
    model = Company
    template_name_suffix = '_update_form'
    template_name = 'cms_mainpage/company_update_form.html'
    fields = ['company_name', 'fio', 'description']



