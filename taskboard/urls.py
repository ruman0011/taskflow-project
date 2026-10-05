from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="taskboard/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path(
        "tasks/<int:task_id>/edit/",
        views.edit_task,
        name="edit_task",
    ),
    path(
        "projects/<int:project_id>/edit/",
        views.edit_project,
        name="edit_project",
    ),
    path("", views.dashboard, name="dashboard"),
]