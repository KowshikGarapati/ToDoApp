from django.urls import path
from . import views

urlpatterns = [
    # Home / Auth Flow
    path("", views.check_if_there_is_any_user_already_logged_in, name="home"),
    path("login/", views.login, name="login"),
    path("login/verify/", views.verify, name="login_verify"),
    path("logout/", views.logout, name="logout"),

    # Signup Flow
    path("signup/", views.signup, name="signup"),
    path("signup/register/", views.register, name="register"),
    path("signup/register/send-email/<str:recipient>/", views.send_verification_email, name="send_verification_email"),
    path("signup/register/verify-otp/", views.verifyotp, name="verify_otp"),
    path("signup/register/verify-email/", views.emailverify, name="email_verify"),

    # Task Management
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/new/", views.newtask, name="new_task"),
    path("tasks/edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),

    # Push Notifications
    path("gps/", views.gpstesting, name="gps_test"),
    path("save_subscription/", views.save_subscription, name="save_subscription"),
    path("send_location_triggered_notification/<int:task_id>/", views.send_location_triggered_notification, name="send_location_triggered_notification"),
    path("send_time_triggered_notification/<int:task_id>/", views.send_time_triggered_notification, name="send_time_triggered_notification"),

    # Service Worker (IMPORTANT: keep this exact name)
    path("service_worker.js", views.service_worker, name="service_worker"),
]
