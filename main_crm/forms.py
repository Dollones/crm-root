from datetime import datetime

from django.forms import ModelForm
from django import forms
from main_crm.models import Company, Phone, Email, Project, Interaction, Profile, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import inlineformset_factory


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
