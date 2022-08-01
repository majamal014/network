
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page>", views.page, name="page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:name>/<int:page>", views.profile, name="profile"),
    path("following/<int:page>", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.update_like, name="like"),
    path("follow/<str:user>", views.follow, name="follow")
]
