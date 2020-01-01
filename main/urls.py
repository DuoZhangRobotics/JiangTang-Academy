from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("about", views.about, name='about'),
    path("register", views.register, name='register'),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name='login'),
    path("contact", views.contact, name='contact'),
    path("courses", views.courses, name='courses'),
    path("account", views.account, name="account"),
    path("account_edit", views.account_edit, name="account_edit"),
    path("change_password", views.change_password, name="change_password"),
    path("edit_info/<username>", views.edit_info, name="edit_info"),
    path("edit_avatar/<username>", views.edit_avatar, name="edit_avatar"),
    # path("profile/<username>", views.profile, name="profile"),
    path("profile/<pk>", views.view_other_profile, name="profile_pk"),
    path("connect/<str:operation>/<int:pk>", views.change_friend, name="change_friends"),
    path("tutorial/<single_slug>", views.single_slug, name="single_slug"),
    path("upload_courses", views.upload_course, name="upload"),
    path("add_category", views.add_category, name="add_cate"),
    path("add_series", views.add_series, name="add_series"),
    path("blog", views.blog, name="blog"),
    path("update_courses/<id>", views.update_courses, name='update'),
    path("delete/<id>", views.delete, name="delete"),
    path("category", views.categories, name="categories"),
    path("series/<pk>", views.series, name="series"),
    path("courses/<pk>", views.courses_series, name="course_series"),
]
