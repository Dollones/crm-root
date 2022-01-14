import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from main_crm.forms import CompanyForm, ProjectForm, InteractionForm, UserForm, ProfileForm, ResetPasswordForm
import tempfile
from PIL import Image


class TestCompanyForm(TestCase):

    def test_company_form_valid_data(self):
        form = CompanyForm(data={
            'company_name': 'Company1',
            'fio': 'FIO1',
            'description': 'Description1',  # Поле description является опциональным
            'started_at': datetime.date(1999, 12, 19),
        })

        self.assertTrue(form.is_valid())

    def test_company_form_no_data(self):
        form = CompanyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestProjectForm(TestCase):

    def test_company_form_valid_data(self):
        form = ProjectForm(data={
            'title': 'Project1',
            'description': 'Description1',  # Поле description является опциональным
            'started_at': datetime.date.today(),
            'cost': 12,  # Поле cost является опциональным
        })
        self.assertTrue(form.is_valid())

    def test_company_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestInteractionForm(TestCase):

    def test_company_interaction_valid_data(self):
        form = InteractionForm(data={
            'channel': 'r',
            'description': 'Description',  # Поле description является опциональным
            'mark': '1',
        })
        self.assertTrue(form.is_valid())

    def test_company_interaction_no_data(self):
        form = InteractionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestProfileForm(TestCase):
    '''
    Вернуться
    '''

    def test_profile_valid_data(self):
        form = ProfileForm(data={
            'profile_image': 'Person1.jpg',
        })
        self.assertTrue(form.data['profile_image'])


class TestUserForm(TestCase):

    def test_company_user_valid_data(self):
        form = UserForm(data={
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'email': 'hfhfhgf@gmail.com',
        })
        self.assertTrue(form.is_valid())

    def test_company_user_no_data_but_valid_too(self):
        form = UserForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEquals(len(form.errors), 0)


class TestResetPasswordForm(TestCase):

    def test_reset_password_valid_data(self):
        user = User.objects.create_user(username='Person1', password='gdfg4234223_1dfgdfgdf', email='hgjh@gmail.com')
        form = ResetPasswordForm(data={
            'username': 'Person1',
        })

        self.assertTrue(User.objects.get(username=form.data['username']) and user.email)
        self.assertTrue(form.is_valid())

    def test_reset_password_account_without_email(self):
        user = User.objects.create_user(username='Person1', password='gdfg4234223_1dfgdfgdf')
        form = ResetPasswordForm(data={
            'username': 'Person1',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(*form.errors['username'], 'This user does not exist or doesn\'t have email account.')

    def test_reset_password_account_does_not_exists(self):
        form = ResetPasswordForm(data={
            'username': 'Person1',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(*form.errors['username'], 'This user does not exist or doesn\'t have email account.')

    def test_reset_password_no_data(self):
        form = ResetPasswordForm(data={})
        self.assertFalse(form.is_valid())
