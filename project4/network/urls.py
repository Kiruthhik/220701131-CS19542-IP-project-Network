
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>",views.view_profile,name="view_profile"),
    path("follow/<str:username>",views.follow,name = "follow"),
    path("following_posts",views.following_page, name="following_posts"),
    path("update_post/<int:id>",views.update_post, name = "update_post"),


    path("likes/<int:id>",views.likes, name = "like"),
]
