from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='index'),
    path('create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('<slug:slug>/delete/', views.CompanyDeleteForm.as_view(), name='company-delete'),
    path('<slug:company_slug>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('<slug:slug>/update/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('<slug:slug>/projects/', views.ProjectListView.as_view(), name='company-projects-list'),
    path('<slug:slug>/projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('<slug:slug>/projects/<int:pk>/delete/', views.ProjectDeleteForm.as_view(), name='project-delete'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/project-interactions/<int:pk>/', views.InteractionListView.as_view(), name='project-interaction-list'),
    path('interactions/interaction/<int:pk>/', views.InteractionDetailView.as_view(), name='interaction-detail'),
    path('<slug:slug>/interactions/', views.CompanyInteractionListView.as_view(), name='company-interactions-list'),
    path('interaction/<int:pk>/create/', views.InteractionCreateView.as_view(), name='interaction-create'),
    path('interaction/<int:pk>/delete/', views.InteractionDeleteForm.as_view(), name='interaction-delete'),
    path('interaction/<int:pk>/update/', views.InteractionUpdateView.as_view(), name='interaction-update'),
]
