from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from usersection.views import getSingleArticle

urlpatterns = [
    path('',HomeView,name="Home"),
    path('contact-us/',ContactUsView.as_view(),name="ContactUs"),
    path('<slug:slug>/',categoryArticles,name="CategoryArticles"),
    path('<slug:categ_slug>/<slug:article_slug>/',getSingleArticle,name="GetSingleArticle"),

    # Password handling related urls (we have put these url in this section because both admin and user will use these views)
    path('u/p/reset_password/',
    auth_views.PasswordResetView.as_view(template_name="password-reset-templates/reset_password.html"),
    name="reset_password"),

    path('u/p/reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="password-reset-templates/reset_password_sent.html"),
    name="password_reset_done"),

    path('u/p/reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-templates/reset_password_form.html"),
    name="password_reset_confirm"),

    path('u/p/password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-templates/reset_password_completed.html"),
    name="password_reset_complete"),

    path('u/p/password_change/',
    auth_views.PasswordChangeView.as_view(template_name="password-reset-templates/password_change.html"),
    name="password_change"),

    path('u/p/password_change_done/',
    auth_views.PasswordChangeDoneView.as_view(template_name="password-reset-templates/password_changed.html"),
    name="password_change_done"),

]
