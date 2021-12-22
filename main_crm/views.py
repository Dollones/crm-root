from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView

from .forms import CompanyForm, PhoneForm, EmailForm
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

    def form_valid(self, form, email_form, phone_form):
        cd = form.cleaned_data
        cd['slug'] = slugify(cd['company_name'])
        self.object = Company.objects.create(**cd)

        email = email_form.save(commit=False)
        phone = phone_form.save(commit=False)
        phone.user = self.object
        email.user = self.object
        phone.save()
        email.save()
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, email_form, phone_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                email_form=email_form,
                phone_form=phone_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        email_form = EmailForm(request.POST)
        phone_form = PhoneForm(request.POST)
        form = self.get_form()

        if form.is_valid() and email_form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, email_form, phone_form)
        else:
            return self.form_invalid(form, email_form, phone_form)

    def get_context_data(self, **kwargs):
        if self.request.method == 'GET':
            kwargs['email_form'] = EmailForm()
            kwargs['phone_form'] = PhoneForm()
        return super().get_context_data(**kwargs)


class CompanyUpdateView(UpdateView):
    queryset = Company.objects.all()
    template_name_suffix = '_update_form'
    template_name = 'cms_mainpage/company_update_form.html'
    fields = ['company_name', 'fio', 'description']

    def form_valid(self, form):
        cd = form.cleaned_data
        cd['slug'] = slugify(cd['company_name'])
        self.object = Company.objects.create(**cd)
        return HttpResponseRedirect(self.get_success_url())

