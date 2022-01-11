import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from main_crm.models import Company, Phone, Email, Project, Interaction, Profile, User


class CompanyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(
            company_name='Company1',
            slug='company1',
            fio='Nikhil Estes',
            description='Desc1',
        )

    def test_company_name_label(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('company_name').verbose_name
        self.assertEquals(field_label, 'Название компании')

    def test_company_name_max_length(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('company_name').max_length
        self.assertEquals(field_label, 150)

    def test_fio_label(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('fio').verbose_name
        self.assertEquals(field_label, 'Руководитель компании')

    def test_fio_max_length(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('fio').max_length
        self.assertEquals(field_label, 150)

    def test_description_label(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_published_label(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('published').verbose_name
        self.assertEquals(field_label, 'Дата публикации')

    def test_edited_label(self):
        company = Company.objects.get(pk=1)
        field_label = company._meta.get_field('edited').verbose_name
        self.assertEquals(field_label, 'Последнее изменение')

    def test_company_str_method(self):
        company = Company.objects.get(pk=1)
        expected_object_name = company.company_name
        self.assertEquals(expected_object_name, str(company))

    def test_company_get_absolute_url(self):
        company = Company.objects.get(pk=1)
        self.assertEquals(company.get_absolute_url(), '/company1/')


class PhoneTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Phone.objects.create(
            user=Company.objects.create(
                company_name='Company1', slug='company1', fio='Nikhil Estes', description='Desc1',
            ),
            phone='42353534543',
        )

    def test_foreign_key_reference(self):
        phone = Phone.objects.get(pk=1)
        field_label = phone.user._meta.get_field('company_name').verbose_name
        self.assertEquals(field_label, 'Название компании')

    def test_user_label(self):
        phone = Phone.objects.get(pk=1)
        field_label = phone._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Компания')

    def test_phone_label(self):
        phone = Phone.objects.get(pk=1)
        field_label = phone._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'Номер телефона')

    def test_phone_max_length(self):
        phone = Phone.objects.get(pk=1)
        field_label = phone._meta.get_field('phone').max_length
        self.assertEquals(field_label, 30)


class EmailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Email.objects.create(
            user=Company.objects.create(
                company_name='Company1', slug='company1', fio='Nikhil Estes', description='Desc1',
            ),
            email='dgdgfd@gmail.com',
        )

    def test_foreign_key_reference(self):
        email = Email.objects.get(pk=1)
        field_label = email.user._meta.get_field('company_name').verbose_name
        self.assertEquals(field_label, 'Название компании')

    def test_user_label(self):
        email = Email.objects.get(pk=1)
        field_label = email._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Компания')

    def test_email_label(self):
        email = Email.objects.get(pk=1)
        field_label = email._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'Адрес электронной почты')

    def test_email_max_length(self):
        email = Email.objects.get(pk=1)
        field_label = email._meta.get_field('email').max_length
        self.assertEquals(field_label, 30)


class ProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(
            user=Company.objects.create(
                company_name='Company1', slug='company1', fio='Nikhil Estes', description='Desc1',
            ),
            title='Project1',
            description='Project1',
            started_at=datetime.date(2023, 6, 21),
            finished_at=datetime.date(2021, 6, 21),
            cost=31313133113,
        )

    def test_user_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Компания')

    def foreign_key_reference(self):
        project = Project.objects.get(pk=1)
        field_label = project.user._meta.get_field('company_name').verbose_name
        self.assertEquals(field_label, 'Название компании')

    def test_title_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название проекта')

    def test_description_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_started_at_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('started_at').verbose_name
        self.assertEquals(field_label, 'Дата начала проекта')

    def test_finished_at_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('finished_at').verbose_name
        self.assertEquals(field_label, 'Дата завершения проекта')

    def test_cost_label(self):
        project = Project.objects.get(pk=1)
        field_label = project._meta.get_field('cost').verbose_name
        self.assertEquals(field_label, 'Затраты на проект')

    def test_project_str_method(self):
        project = Project.objects.get(pk=1)
        expected_object_name = project.title
        self.assertEquals(expected_object_name, str(project))

    def test_project_get_absolute_url(self):
        project = Project.objects.get(pk=1)
        self.assertEquals(project.get_absolute_url(), '/project/1/')

    def test_project_clean_method(self):
        project = Project.objects.get(pk=1)
        with self.assertRaises(ValidationError) as e:
            project.clean()
        self.assertEquals('Started_at can`t be bigger then finished_at', e.exception.args[0]['started_at'])


class InteractionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Interaction.objects.create(
            project=Project.objects.create(
                user=Company.objects.create(
                    company_name='Company1', slug='company1', fio='Nikhil Estes', description='Desc1',
                ),
                title='Project1',
                description='Project1',
                started_at=datetime.date(2021, 6, 21),
                finished_at=datetime.date(2023, 6, 21),
                cost=31313133113,
            ),
            channel='r',

            manager=User.objects.create_user(
                username='Alan',
                email='fhdskfh@rambler.ru',
                password='ert54i_42'
            ),
            description='Descriptongklg',
            mark='1',
        )

    def test_project_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('project').verbose_name
        self.assertEquals(field_label, 'Проект')

    def test_channel_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('channel').verbose_name
        self.assertEquals(field_label, 'Канал обращения')

    def test_manager_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('manager').verbose_name
        self.assertEquals(field_label, 'Менеджер')

    def test_description_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_mark_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('mark').verbose_name
        self.assertEquals(field_label, 'Оценка')

    def test_created_at_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_updated_at_label(self):
        interaction = Interaction.objects.get(pk=1)
        field_label = interaction._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'Дата редактирования')

    def test_interaction_get_absolute_url(self):
        interaction = Interaction.objects.get(pk=1)
        self.assertEquals(interaction.get_absolute_url(), '/interactions/interaction/1/')

    def test_interaction_str_method(self):
        interaction = Interaction.objects.get(pk=1)
        self.assertEquals(interaction.description, str(interaction))


class ProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Alan',
            email='fhdskfh@rambler.ru',
            password='ert54i_42',
        )
        Profile.objects.create(
            user=user,
            profile_image='main_crm/static/images/default.png',
        )

    def test_user_label(self):
        profile = Profile.objects.get(pk=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_foreign_key_reference(self):
        profile = Profile.objects.get(pk=1)
        field_label = profile.user.username
        self.assertEquals(field_label, 'Alan')

    def test_profile_image_label(self):
        profile = Profile.objects.get(pk=1)
        field_label = profile._meta.get_field('profile_image').verbose_name
        self.assertEquals(field_label, 'Аватар')

    def test_profile_image(self):
        profile = Profile.objects.get(pk=1)
        self.assertIsNotNone(profile.profile_image)

    def test_profile_str_method(self):
        profile = Profile.objects.get(pk=1)
        expected_object_name = profile.user.username
        self.assertEquals(expected_object_name, str(profile))
