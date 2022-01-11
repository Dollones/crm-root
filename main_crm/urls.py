from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as dj_views

urlpatterns = [
    path('projects/<int:pk>/delete/', views.ProjectDeleteForm.as_view(), name='project-delete'),
    path('mym-profile/', views.UserInteractionListView.as_view(), name='manager-profile'),
    path('my-profile/password-change/', views.UserPasswordChangeView.as_view(), name='password-change'),

    path('password-reset/', include([
        path('', views.UserResetPassword.as_view(), name='password-reset'),
        path('done/',
             dj_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_confirm.html'),
             name='password_reset_done'),
        re_path(r'^confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', dj_views.PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'),
        path('complete/',
             dj_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
             name='password_reset_complete'),
    ])),

    path('register/', include([
        path('', views.UserSignUp.as_view(), name='register'),
        path('success/', views.UserSignUpSuccess.as_view(), name='register-success'),
    ])),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('', views.CompanyListView.as_view(), name='index'),
    path('all-projects/', views.AllProjectsListView.as_view(), name='all-projects'),
    path('create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('all-interactions/', views.AllInteractionListView.as_view(), name='all-interaction-list'),
    path('profile/update/', views.UpdateUserView.as_view(), name='profile-update'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/project-interactions/<int:pk>/', views.InteractionListView.as_view(),
         name='project-interaction-list'),
    path('interactions/interaction/<int:pk>/', views.InteractionDetailView.as_view(), name='interaction-detail'),
    path('interaction/', include([
        path('<int:pk>/create/', views.InteractionCreateView.as_view(), name='interaction-create'),
        path('<int:pk>/delete/', views.InteractionDeleteForm.as_view(), name='interaction-delete'),
        path('<int:pk>/update/', views.InteractionUpdateView.as_view(), name='interaction-update'),
    ])),

    path('<slug:slug>/', include([
        path('', views.CompanyDetailView.as_view(), name='company-detail'),
        path('update/', views.CompanyUpdateView.as_view(), name='company-update'),
        path('delete/', views.CompanyDeleteForm.as_view(), name='company-delete'),
        path('projects/', views.ProjectListView.as_view(), name='company-projects-list'),
        path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
        path('interactions/', views.CompanyInteractionListView.as_view(), name='company-interactions-list'),
    ])),
]
