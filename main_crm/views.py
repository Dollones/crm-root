import copy
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import CompanyForm, ProjectForm, InteractionForm, ProfileForm, UserForm, \
    CreateEmailFormSet, CreatePhoneFormSet, UpdateEmailFormSet, UpdatePhoneFormSet
from .models import Company, Project, Interaction, User, Phone, Email
from .const import INDEX_PAGINATE_BY
from .filters import CompanyFilter, InteractionFilter
from .utils import slugify
from .permissions import SuperUserRequired, OwnerRequired
from django.contrib.auth.mixins import LoginRequiredMixin


class CompanyListView(LoginRequiredMixin, FilterView):
    """
    Контроллер для вывода списка компаний на главной странице
    """
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/list_page.html'
    paginate_by = INDEX_PAGINATE_BY
    filterset_class = CompanyFilter

    def get_context_data(self, *args, **kwargs):
        """
        Перопределенный метод для совместимости фильтров и пагинации
        :param args:
        :param kwargs:
        :return:
        """
        sort_by = self.request.GET.get('sort_by', '')
        sort_by_param = f'&sort_by={sort_by}'
        return super().get_context_data(*args, sort_by_param=sort_by_param, **kwargs)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для вывода детальной информации о компании
    """
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/detail_page.html'
    slug_url_kwarg = 'company_slug'


class CompanyCreateView(LoginRequiredMixin, SuperUserRequired, CreateView):
    """
    Контроллер для создания компании
    """
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/create_company.html'
    form_class = CompanyForm

    def form_valid(self, form, email_form, phone_form):
        """
        Переопределенный метод для проверки форм на валидность
        :param form:
        :param email_form:
        :param phone_form:
        :return:
        """
        cd = form.cleaned_data
        cd['slug'] = slugify(cd['company_name'])
        self.object = Company.objects.create(**cd)

        emails = email_form.save(commit=False)
        phones = phone_form.save(commit=False)

        for phone in phones:
            phone.user = self.object

        for email in emails:
            email.user = self.object

        Phone.objects.bulk_create(phones)
        Email.objects.bulk_create(emails)

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
        """
        Метод обработки запроса для создания модели Company и связанных с ней Email и Phone
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = None
        email_form = CreateEmailFormSet(request.POST)
        phone_form = CreatePhoneFormSet(request.POST)
        form = self.get_form()

        if form.is_valid() and email_form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, email_form, phone_form)
        else:
            return self.form_invalid(form, email_form, phone_form)

    def get_context_data(self, **kwargs):
        """
        Метод для передачи форм CreateEmailFormSet и CreatePhoneFormSet в контекст шаблона
        :param kwargs:
        :return:
        """
        if self.request.method == 'GET':
            kwargs['email_form'] = CreateEmailFormSet()
            kwargs['phone_form'] = CreatePhoneFormSet()
        return super().get_context_data(**kwargs)


class CompanyDeleteForm(LoginRequiredMixin, SuperUserRequired, DeleteView):
    """
    Контроллер для удаления модели Company и связанных с ней Email и Phone
    """
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/company_delete.html'

    success_url = reverse_lazy('index')
    raise_exception = True


class CompanyUpdateView(LoginRequiredMixin, SuperUserRequired, UpdateView):
    """
    Контроллер для обновления данных модели Company и связанных с ней Email и Phone
    """
    queryset = Company.objects.all()
    template_name = 'cms_mainpage/company_update_form.html'
    form_class = CompanyForm

    def form_valid(self, form, email_form, phone_form):
        """
        Переопределенный метод,который проверяет формы на валидность
        :param form:
        :param email_form:
        :param phone_form:
        :return:
        """
        company = form.save(commit=False)
        cd = form.cleaned_data
        company.slug = slugify(cd['company_name'])
        company.save()

        email_form.save()
        phone_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, email_form, phone_form):
        """
        Переопределенный метод,который возвращает данные пользователя,если они не прошли валидность
        :param form:
        :param email_form:
        :param phone_form:
        :return:
        """
        return self.render_to_response(
            self.get_context_data(
                form=form,
                email_form=email_form,
                phone_form=phone_form
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Метод обработки запроса для обновления модели Company и связанных с ней Email и Phone
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = company = self.get_object()
        form = self.get_form()

        email_form = UpdateEmailFormSet(request.POST, instance=company)
        phone_form = UpdatePhoneFormSet(request.POST, instance=company)

        if form.is_valid() and email_form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, email_form, phone_form)
        else:
            return self.form_invalid(form, email_form, phone_form)

    def get_context_data(self, **kwargs):
        """
        Метод для добавления в контекс шаблона форм UpdateEmailFormSet и UpdatePhoneFormSet со старыми данными
        :param kwargs:
        :return:
        """
        if self.request.method == 'GET':
            company = self.get_object()
            kwargs['email_form'] = UpdateEmailFormSet(instance=company)
            kwargs['phone_form'] = UpdatePhoneFormSet(instance=company)

        return super().get_context_data(**kwargs)


class ProjectListView(LoginRequiredMixin, ListView):
    """
    Контроллер для вывода списка проектов конкретной компании
    """
    context_object_name = 'projects'
    template_name = 'cms_mainpage/project_list_page.html'

    def get_queryset(self):
        """
        Метод для возврата списка проектов конкретной компании
        :return:
        """
        return Project.objects.filter(user__slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        """
        Метод для добавления в контекст шаблона данных с ссылки
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        return context


class AllProjectsListView(LoginRequiredMixin, ListView):
    """
    Контроллер для вывода всех существующих проектов
    """
    template_name = 'cms_mainpage/all-projects.html'

    def get_queryset(self):
        """
        Метод для возврата списка всех проектов
        :return:
        """
        return Project.objects.all()


class ProjectDetailView(LoginRequiredMixin, SuperUserRequired, DetailView):
    """
    Контроллер для вывода детальной информации о проекте
    """
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, SuperUserRequired, CreateView):
    """
    Контроллер для создания проекта
    """
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/create_project.html'
    form_class = ProjectForm
    raise_exception = True

    def form_valid(self, form):
        """
        Метод для проверки формы на валидность
        :param form:
        :return:
        """
        self.object = project = form.save(commit=False)
        project.user = Company.objects.get(slug=self.kwargs['slug'])
        project.save()
        messages.success(self.request, 'Проект создан')
        return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteForm(LoginRequiredMixin, SuperUserRequired, DeleteView):
    """
    Контроллер для удаления модели Project
    """
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_delete.html'
    raise_exception = True

    def get_success_url(self):
        """
        Метод для перенаправления пользователя на страницу всех проектов компании после удаления записи
        :return:
        """
        slug = self.object.user.slug
        success_url = reverse_lazy('company-projects-list', kwargs={'slug': slug})
        return success_url


class ProjectUpdateView(LoginRequiredMixin, SuperUserRequired, UpdateView):
    """
    Контроллер для обновления информации модели Project
    """
    queryset = Project.objects.all()
    template_name = 'cms_mainpage/project_update_form.html'
    form_class = ProjectForm
    raise_exception = True


class InteractionListView(LoginRequiredMixin, SuperUserRequired, ListView):
    """
    Контроллер для вывода списка всех взаимодействий
    """
    template_name = 'cms_mainpage/interaction_list_page.html'
    paginate_by = INDEX_PAGINATE_BY
    queryset = Interaction.objects.all()

    def get_queryset(self):
        """
        Контроллер,который возвращает список всех взаимодействий конкретного проекта
        :return:
        """
        return super().get_queryset().filter(project__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Метод для передачи информации с ссылки в контекст шаблона
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class InteractionDetailView(LoginRequiredMixin, SuperUserRequired, DetailView):
    """
    Контроллер для вывода детальной информации о конкретном взаимодействии
    """
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_detail.html'


class CompanyInteractionListView(LoginRequiredMixin, SuperUserRequired, ListView):
    """
    Контроллер для просмотра всех взаимодействий конкретной компании
    """
    template_name = 'cms_mainpage/company_interaction_list_page.html'

    def get_queryset(self):
        """
        Метод,который возвращает отфильтрованный  список взаимодействий по слагу компании в ссылке
        :return:
        """
        return Interaction.objects.filter(project__user__slug=self.kwargs['slug'])


class InteractionCreateView(LoginRequiredMixin, SuperUserRequired, CreateView):
    """
    Контроллер для создания модели Interaction
    """
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/create_interaction.html'
    form_class = InteractionForm
    raise_exception = True

    def form_valid(self, form):
        """
        Метод для проверки формы на валидность
        :param form:
        :return:
        """
        self.object = interaction = form.save(commit=False)
        interaction.manager = self.request.user
        interaction.project = Project.objects.get(pk=self.kwargs['pk'])
        interaction.save()
        messages.success(self.request, 'Взаимодействие создано')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Метод для перенаправления пользователя на страницу всех взаимодействий проекта
        :return:
        """
        pk = self.kwargs['pk']
        success_url = reverse_lazy('project-interaction-list', kwargs={'pk': pk})
        return success_url


class InteractionDeleteForm(LoginRequiredMixin, SuperUserRequired, OwnerRequired, DeleteView):
    """
    Контроллер для удаления модели Interaction
    """
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_delete.html'
    raise_exception = True
    user_field = 'manager'

    def get_success_url(self):
        """
        Метод для перенаправления пользователя на страницу всех взаимодействи проекта
        :return:
        """
        success_url = reverse_lazy('project-interaction-list', kwargs={'pk': self.object.project.id})
        return success_url


class InteractionUpdateView(LoginRequiredMixin, SuperUserRequired, OwnerRequired, UpdateView):
    """
    Контроллер для обновления информации в модели Interaction
    """
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/interaction_update_form.html'
    form_class = InteractionForm
    raise_exception = True
    user_field = 'manager'


class AllInteractionListView(LoginRequiredMixin, SuperUserRequired, FilterView):
    """
    Контроллер для вывода всех взаимодействий
    """
    queryset = Interaction.objects.all()
    template_name = 'cms_mainpage/all_interaction_list.html'
    filterset_class = InteractionFilter
    paginate_by = INDEX_PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        """
        Метод для учета правильной работы фильтров и пагинации
        :param args:
        :param kwargs:
        :return:
        """
        params_string = ''
        get_params = copy.copy(self.request.GET)
        get_params.pop('page', False)

        if get_params:

            get_string_elems = []
            get_prams_iter = iter(get_params.items())

            key, values = next(get_prams_iter, (None, None))

            while key:
                [get_string_elems.append(f'&{key}={value}') for value in values]
                key, values = next(get_prams_iter, (None, None))

            params_string = ''.join(get_string_elems)

        return super().get_context_data(*args, params_string=params_string, **kwargs)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для обновления информации в модели User
    """
    template_name = 'cms_mainpage/update_profile.html'
    form_class = UserForm
    profile_form = None
    success_url = reverse_lazy('manager-profile')
    raise_exception = True

    def get_object(self):
        """
        Метод для получения объекта пользователя
        :return:
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Метод для передачи формы обновления пользователя в контекст шаблона
        :param kwargs:
        :return:
        """
        if self.request.method == 'GET':
            user = self.get_object()
            profile = user.profile
            kwargs['profile_form'] = ProfileForm(instance=profile)

        return super().get_context_data(**kwargs)

    def form_valid(self, form, profile_form):
        """
        Метод для проверки формы на валидность
        :param form:
        :param profile_form:
        :return:
        """
        self.object = form.save()

        profile = profile_form.save(commit=False)
        profile.user = self.object
        profile.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_form):
        return self.render_to_response(
            self.get_context_data(
                form=form, profile_form=profile_form,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Метод обработки запроса для обновления модели User
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        form = self.get_form()

        profile = self.object.profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)


class UserInteractionLitView(LoginRequiredMixin, DetailView):
    """
    Контроллер для вывода информации о пользователе(профиль пользователя) и всех записей,которые
    он создал(компании,проекты и взаимодействия)
    """
    queryset = User.objects.all()
    template_name = 'cms_mainpage/manager_profile.html'

    def get_object(self):
        """
        Метод для получения объекта пользователя
        :return:
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Метод для передачи списка взаимодействий,которые создал пользователь
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['interactions'] = Interaction.objects.filter(manager=self.object)
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Контроллер для смены пароля пользователя
    """
    template_name = 'cms_mainpage/password_change.html'
    success_url = reverse_lazy('manager-profile')

    def get_success_url(self):
        """
        Метод для перенаправления пользователя на страницу профиля
        :return:
        """
        messages.success(self.request, 'Ваш пароль успешно изменён!')
        return super(UserPasswordChangeView, self).get_success_url()


class LoginUser(LoginView):
    """
    Контроллер для вывода страницы авторизации пользователя
    """
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        """
        Метод для перенаправления пользователя на главную страницу после авторизации
        :return:
        """
        return reverse_lazy('index')


def logout_user(request):
    """
    Функция-контроллер для выхода учетной записи пользователя с сайта
    :param request:
    :return:
    """
    logout(request)
    return redirect('login')
