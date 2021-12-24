from datetime import datetime

from django.forms import ModelForm
from django import forms
from main_crm.models import Company, Phone, Email, Project, Interaction
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
