from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='index'),
    path('create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('<slug:company_slug>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('<slug:slug>/update/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('<slug:slug>/projects/', views.ProjectListView.as_view(), name='company-projects-list'),
    path('<slug:slug>/projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
]
