from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
import datetime

from main_crm.models import Company, Phone, Email, Project, Interaction


class CompanyListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.user = User.objects.create_user(username='GGGGGG', password='qweqweqweqwe')

    def test_project_list_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/list_page.html')


class CompanyDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.company_detail_url = reverse('company-detail', args=['company1'])
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_list_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.company_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/detail_page.html')


class CompanyCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company_create_url = reverse('company-create')
        self.redirect_url = reverse('company-detail', args=['company1'])
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_company_create_POST_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.company_create_url, {
            'company_name': 'Company1',
            'fio': 'GDFGHBLR',
            'description': 'Description',
            'email_set-TOTAL_FORMS': '2',
            'email_set-INITIAL_FORMS': '0',
            'email_set-MIN_NUM_FORMS': '0',
            'email_set-MAX_NUM_FORMS': '1000',
            'email_set-0-email': 'mail1@gmail.com',
            'email_set-0-id': '',
            'email_set-0-user': '',
            'email_set-1-email': 'gmjf@gmwerwerweil.com',
            'email_set-1-id ': '',
            'email_set - 1 - user': '',
            'phone_set-TOTAL_FORMS': '2',
            'phone_set-INITIAL_FORMS': '0',
            'phone_set-MIN_NUM_FORMS': '0',
            'phone_set-MAX_NUM_FORMS': '1000',
            'phone_set-0-phone': '+3213482439',
            'phone_set-0-id': '',
            'phone_set-0-user': '',
            'phone_set-1-phone': '',
            'phone_set-1-id ': '',
            'phone_set - 1 - user': '',
        })

        company = Company.objects.last()

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        self.assertEquals(Company.objects.all().count(), 1)
        self.assertEquals(company.company_name, 'Company1')
        self.assertEquals(company.fio, 'GDFGHBLR')
        self.assertEquals(company.description, 'Description')
        self.assertEquals(company.slug, 'company1')
        self.assertEquals(company.phone_set.first().phone, '+3213482439')
        self.assertEquals(company.email_set.first().email, 'mail1@gmail.com')
        self.assertEquals(company.email_set.last().email, 'gmjf@gmwerwerweil.com')

    def test_company_create_POST_method_no_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.company_create_url)
        self.assertNotEquals(response.status_code, 302)
        self.assertEquals(Company.objects.all().count(), 0)


class CompanyDeleteFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company_delete_url = reverse('company-delete', args=['company1'])
        self.redirect_url = reverse('index')
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_company_DELETE_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )

        response = self.client.delete(self.company_delete_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        self.assertEquals(Company.objects.all().count(), 0)


class CompanyUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        Phone.objects.bulk_create([
            Phone(user=self.company, phone='1233124'),
            Phone(user=self.company, phone='+12325446424'),
        ])

        Email.objects.bulk_create([
            Email(user=self.company, email='gdfjh@gmail.com'),
            Email(user=self.company, email='ewfsfsd@rambler.ru'),
        ])
        self.company_update_url = reverse('company-update', args=['company1'])
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.redirect_url = reverse('company-detail', args=['changedcompanyname'])

    def test_company_update_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.company_update_url, {
            'company_name': 'ChangedCompanyName',
            'fio': 'Nikhil Estes',
            'description': 'Desc1',
            'email_set-TOTAL_FORMS': '2',
            'email_set-INITIAL_FORMS': '2',
            'email_set-MIN_NUM_FORMS': '0',
            'email_set-MAX_NUM_FORMS': '2',
            'email_set-0-email': 'gdfjh@gmail.com',
            'email_set-0-id': '1',
            'email_set-0-user': '1',
            'email_set-1-email': 'ewfsfsd@rambler.ru',
            'email_set-1-DELETE': 'on',
            'email_set-1-id ': '2',
            'email_set-1-user': '1',
            'phone_set-TOTAL_FORMS': '2',
            'phone_set-INITIAL_FORMS': '2',
            'phone_set-MIN_NUM_FORMS': '0',
            'phone_set-MAX_NUM_FORMS': '2',
            'phone_set-0-phone': '1233124',
            'phone_set-0-id': '1',
            'phone_set-0-user': '1',
            'phone_set-1-phone': '+12325446424',
            'phone_set-1-DELETE': 'on',
            'phone_set-1-id ': '2',
            'phone_set - 1 - user': '1',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        self.assertEquals(Company.objects.all().count(), 1)
        company = Company.objects.last()
        self.assertEquals(len(company.phone_set.all()), 1)
        self.assertEquals(len(company.email_set.all()), 1)
        self.assertNotEquals(company.company_name, 'Company1')
        self.assertNotEquals(company.slug, 'company1')


class ProjectListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.projects_list_url = reverse('company-projects-list', args=['company1'])
        self.user = User.objects.create_user(username='GGGGGG', password='qweqweqweqwe')

    def test_project_list_GET(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.projects_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/project_list_page.html')


class AllProjectsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.all_projects_list_url = reverse('all-projects')
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_all_project_list_GET(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.all_projects_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/all-projects.html')


class ProjectDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.company = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )
        self.projects_detail_url = reverse('project-detail', args=['1'])
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_detail_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.projects_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/project_detail.html')


class ProjectCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project_create_url = reverse('project-create', args=['company1'])
        self.redirect_url = reverse('project-detail', args=['1'])
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_create_POST_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.project_create_url, {
            'title': 'Project1',
            'description': 'Description1',
            'started_at_month': '12',
            'started_at_day': '21',
            'started_at_year': '1991',
            'finished_at_month': '11',
            'finished_at_day': '20',
            'finished_at_year': '2002',
            'cost': '1213'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        project = Project.objects.last()
        self.assertEquals(Project.objects.all().count(), 1)
        self.assertEquals(project.title, 'Project1')

    def test_project_create_POST_method_no_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.project_create_url)
        self.assertNotEquals(response.status_code, 302)
        self.assertEquals(Project.objects.all().count(), 0)


class ProjectDeleteFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )
        self.projects_delete_url = reverse('project-delete', args=['1'])
        self.redirect_url = reverse('company-projects-list', args=['company1'])
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_DELETE_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.delete(self.projects_delete_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        self.assertEquals(Project.objects.all().count(), 0)


class ProjectUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )
        self.projects_update_url = reverse('project-update', args=['1'])
        self.redirect_url = reverse('project-detail', args=['1'])
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_update_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.projects_update_url, {
            'title': 'ChangedProjectTitle',
            'description': 'dsjfsdj',
            'started_at_month': '9',
            'started_at_day': '16',
            'started_at_year': '1999',
            'finished_at_month': '',
            'finished_at_day': '',
            'finished_at_year': '',
            'cost': '8',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        self.assertEquals(Project.objects.all().count(), 1)
        project = Project.objects.last()
        self.assertNotEquals(project.title, 'Project1')
        self.assertEquals(project.title, 'ChangedProjectTitle')


class InteractionListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',

        )
        self.interaction_list_url = reverse('project-interaction-list', args=['1'])

    def test_interaction_list_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.interaction_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/interaction_list_page.html')


class InteractionDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',

        )
        self.interaction_detail_url = reverse('interaction-detail', args=['1'])

    def test_interaction_detail_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.interaction_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/interaction_detail.html')


class CompanyInteractionListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',
        )
        self.company_interactions_list_url = reverse('company-interactions-list', args=['company1'])

    def test_company_interaction_list_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.company_interactions_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/company_interaction_list_page.html')


class InteractionCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )
        self.interactions_create_url = reverse('interaction-create', args=['1'])
        self.redirect_url = reverse('project-interaction-list', args=['1'])

    def test_interaction_create_POST_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.interactions_create_url, {
            'channel': 'w',
            'description': 'Description1',
            'mark': '2',
        })
        self.assertEquals(response.status_code, 302)

        interaction = Interaction.objects.last()
        self.assertEquals(interaction.channel, 'w')
        self.assertEquals(interaction.description, 'Description1')
        self.assertEquals(interaction.get_mark_display(), 'Плохо')

    def test_interaction_create_POST_method_no_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.interactions_create_url)

        self.assertNotEquals(response.status_code, 302)
        self.assertEquals(Interaction.objects.all().count(), 0)


class InteractionDeleteFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',
        )
        self.interactions_delete_url = reverse('interaction-delete', args=['1'])
        self.redirect_url = reverse('project-interaction-list', args=['1'])

    def test_interaction_DELETE_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.delete(self.interactions_delete_url)
        self.assertEquals(Interaction.objects.all().count(), 0)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)


class InteractionUpdateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',
        )
        self.interactions_update_url = reverse('interaction-update', args=['1'])
        self.redirect_url = reverse('interaction-detail', args=['1'])

    def test_interaction_update_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.interactions_update_url, {
            'channel': 'w',
            'description': 'Desc2',
            'mark': '2',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        self.assertEquals(Interaction.objects.all().count(), 1)
        interaction = Interaction.objects.last()
        self.assertEquals(interaction.channel, 'w')
        self.assertEquals(interaction.description, 'Desc2')
        self.assertEquals(interaction.mark, '2')


class AllInteractionListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.company = Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )
        self.project = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )

        self.interaction = Interaction.objects.create(
            project=self.project,
            channel='r',
            manager=self.user,
            description='Desc1',
            mark='1',
        )
        self.all_interactions_url = reverse('all-interaction-list')

    def test_all_interaction_list_GET_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.all_interactions_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms_mainpage/all_interaction_list.html')


# class UpdateUserViewTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe', email='dfdfsd@rambler.ru')
#         self.all_interactions_url = reverse('profile-update')
#
#     def test_profile_change_data(self):
#         self.client.login(username='GGGGGG', password='qweqweqweqwe')


class UserPasswordChangeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe', email='dfdfsd@rambler.ru')
        self.change_password_url = reverse('password-change')
        self.redirect_url = reverse('manager-profile')

    def test_password_change(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.post(self.change_password_url, {
            'old_password': 'qweqweqweqwe',
            'new_password1': '65rewsdfghjtr',
            'new_password2': '65rewsdfghjtr',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

        self.client.logout()
        self.assertFalse(self.client.login(username='GGGGGG', password='qweqweqweqwe'))
        self.assertTrue(self.client.login(username='GGGGGG', password='65rewsdfghjtr'))


class LoginUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_login(self):
        login_correct = self.client.login(username='GGGGGG', password='qweqweqweqwe')
        login_wrong = self.client.login(username='GefgrGG', password='qwe42534qweqweqwe')
        self.assertTrue(login_correct)
        self.assertFalse(login_wrong)


class LogoutUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')
        self.login_url = reverse('index')

    def test_logout(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        self.client.logout()
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 302)


class UserSignUpTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.redirect_url = reverse('register-success')

    def test_user_sign_up_POST_method(self):
        response = self.client.post(self.register_url, {
            'username': 'user1',
            'password1': '32ttyuewq235A_',
            'password2': '32ttyuewq235A_',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        self.assertEquals(User.objects.all().count(), 1)
