from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from main_crm.models import Company, Phone, Email, Project, Interaction, Profile, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserModel
from django.contrib.auth.forms import _


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('slug',)
        widgets = {
            'description': CKEditorUploadingWidget(),
        }


class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = ('user',)


class EmailForm(ModelForm):
    class Meta:
        model = Email
        exclude = ('user',)


CreatePhoneFormSet = inlineformset_factory(
    Company,
    Phone,
    fields=('phone',),
    extra=2,
    can_delete=False
)

UpdatePhoneFormSet = inlineformset_factory(
    Company,
    Phone,
    fields=('phone',),
    extra=2,
    max_num=2,
    can_delete=True
)

CreateEmailFormSet = inlineformset_factory(
    Company,
    Email,
    fields=('email',),
    extra=2,
    can_delete=False
)

UpdateEmailFormSet = inlineformset_factory(
    Company,
    Email,
    fields=('email',),
    extra=2,
    max_num=2,
    can_delete=True
)


class ProjectForm(ModelForm):
    started_at = forms.DateField(widget=forms.SelectDateWidget)
    finished_at = forms.DateField(widget=forms.SelectDateWidget(), required=False)

    class Meta:
        model = Project
        exclude = ('user',)
        widgets = {
            'description': CKEditorUploadingWidget(),
        }


class InteractionForm(ModelForm):
    class Meta:
        model = Interaction
        fields = ('channel', 'description', 'mark')
        widgets = {
            'description': CKEditorUploadingWidget(),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_image',)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ResetPasswordForm(PasswordResetForm):
    email = None
    username = forms.CharField(
        label=_("Username"),
        max_length=254,
    )

    def get_users(self, username):
        return User.objects.get(username=username)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        username = self.cleaned_data["username"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        user = self.get_users(username)
        user_email = getattr(user, email_field_name)
        context = {
            'email': user_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        self.send_mail(
            subject_template_name, email_template_name, context, from_email,
            user_email, html_email_template_name=html_email_template_name,
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists() or not User.objects.get(username=username).email:
            raise ValidationError(_('This user does not exist or doesn\'t have email account.'), code='invalid')
        return username
