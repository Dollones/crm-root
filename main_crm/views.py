from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django_filters.views import FilterView

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import CompanyForm, PhoneForm, EmailForm, ProjectForm, InteractionForm
from .models import Company, Project, Interaction
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


class CompanyDetailView(DetailView):
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


class CompanyDeleteForm(DeleteView):
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/company_delete.html'

    success_url = reverse_lazy('index')


class CompanyUpdateView(UpdateView):
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/company_update_form.html'
    form_class = CompanyForm
    email_form = None
    phone_form = None

    def form_valid(self, form, email_form, phone_form):
        company = form.save(commit=False)
        cd = form.cleaned_data
        company.slug = slugify(cd['company_name'])
        company.save()

        email_form.save()
        phone_form.save()
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
        self.object = self.get_object()
        form = self.get_form()

        email = self.object.email_set.first()
        email_form = EmailForm(request.POST, instance=email)

        phone = self.object.phone_set.first()
        phone_form = PhoneForm(request.POST, instance=phone)

        if form.is_valid() and email_form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, email_form, phone_form)
        else:
            return self.form_invalid(form, email_form, phone_form)

    def get_context_data(self, **kwargs):
        if self.request.method == 'GET':
            company = self.get_object()
            email = company.email_set.first()
            phone = company.phone_set.first()
            kwargs['email_form'] = EmailForm(instance=email)
            kwargs['phone_form'] = PhoneForm(instance=phone)

        return super().get_context_data(**kwargs)


class ProjectListView(ListView):
    context_object_name = 'projects'
    template_name = 'cms_mainpage/project_list_page.html'

    def get_queryset(self):
        return Project.objects.filter(user__slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        return context


class ProjectDetailView(DetailView):
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_detail.html'


class ProjectCreateView(CreateView):
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/create_project.html'
    form_class = ProjectForm

    def form_valid(self, form):
        self.object = project = form.save(commit=False)
        project.user = Company.objects.get(slug=self.kwargs['slug'])
        project.save()
        messages.success(self.request, 'Проект создан')
        return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteForm(DeleteView):
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_delete.html'

    def get_success_url(self):
        slug = self.kwargs['slug']
        success_url = reverse_lazy('company-projects-list', kwargs={'slug': slug})
        return success_url


class ProjectUpdateView(UpdateView):
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_update_form.html'
    form_class = ProjectForm


class InteractionListView(ListView):
    template_name = 'cms_mainpage/interaction_list_page.html'
    paginate_by = INDEX_PAGINATE_BY

    def get_queryset(self):
        return Interaction.objects.filter(project__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class InteractionDetailView(DetailView):
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_detail.html'


class CompanyInteractionListView(ListView):
    template_name = 'cms_mainpage/company_interaction_list_page.html'

    def get_queryset(self):
        return Interaction.objects.filter(project__user__slug=self.kwargs['slug'])


class InteractionCreateView(CreateView):
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/create_interaction.html'
    form_class = InteractionForm

    def form_valid(self, form):
        self.object = interaction = form.save(commit=False)
        interaction.manager = self.request.user
        interaction.project = Project.objects.get(pk=self.kwargs['pk'])
        interaction.save()
        messages.success(self.request, 'Взаимодействие создано')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pk = self.kwargs['pk']
        success_url = reverse_lazy('project-interaction-list', kwargs={'pk': pk})
        return success_url


class InteractionDeleteForm(DeleteView):
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_delete.html'

    def get_success_url(self):
        success_url = reverse_lazy('project-interaction-list', kwargs={'pk': self.object.project.id})
        return success_url


class InteractionUpdateView(UpdateView):
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_update_form.html'
    form_class = InteractionForm
