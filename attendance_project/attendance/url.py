from django.urls import path, include,re_path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings


urlpatterns = [
    path('', views.home_attendance,name='attendance-home'),
    path('user_window', views.user_window, name='user-window'),
    re_path(r'^create_employee_detail/(\w+)/$',
         views.create_employee_detail, name='create-employee-detail'),
    re_path(r'^mark_attendance/(\w+)/$',
            views.mark_attendance, name='mark-attendance'),
    re_path(r'^apply_leaves/(\w+)/$',
            views.apply_leaves, name='apply-leaves'),
    path('signup', views.sign_up_form, name='signup'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('logout/', auth_view.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_view.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-compelete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
