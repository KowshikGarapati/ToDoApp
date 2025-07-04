from django.urls import path
from . import views


urlpatterns = [
       path("", views.check_if_there_is_any_user_already_logged_in, name="checkifuserloggedin"),
       path('tasks/', views.task_list, name="task_list"),
       path('newtask/', views.newtask),
       path('savenewtask/', views.savenewtask),
       path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
       path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
       path("login/", views.login, name="login"),
       path("logout/", views.logout, name="logout"),
       path("login/verify/", views.verify, name="login_verify"),
       path('signup/', views.signup, name='signup'),
       path('signup/register/', views.register, name='register'),
       path('signup/register/emailverify/', views.emailverify, name='emailverify'),
       path('signup/register/sendverificationemail/<str:recipient>', views.send_verification_email, name='sendverificationemail'),
       path('signup/register/verifyotp', views.verifyotp, name='verifyotp'),#path("", views., name=""),
       path('gps/', views.gpstesting),
    ]
