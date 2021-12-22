from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='index'),
    path('create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('<slug:company_slug>/', views.CompanyDetialView.as_view(), name='company-detail'),
]
