from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
import datetime

from main_crm.models import Company, Phone, Email, Project


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
    '''
    Вернуться
    '''

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
        self.redirect_url = reverse('company-update', args=['company1'])
        self.super_user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_company_update_data(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.get(self.company_update_url)


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
        self.company = Project.objects.create(
            user=self.company,
            title='Project1',
            description='Description1',
            started_at=datetime.date(1991, 12, 21),
            finished_at=datetime.date(2002, 11, 20),
            cost=1213,
        )
        self.projects_delete_url = reverse('project-delete', kwargs={'slug': 'comp', 'pk': '1'})
        self.redirect_url = reverse('company-projects-list', args=['company1'])
        self.user = User.objects.create_superuser(username='GGGGGG', password='qweqweqweqwe')

    def test_project_DELETE_method(self):
        self.client.login(username='GGGGGG', password='qweqweqweqwe')
        response = self.client.delete(self.projects_delete_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        self.assertEquals(Project.objects.all().count(), 0)
