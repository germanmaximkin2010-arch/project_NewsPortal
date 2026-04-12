from django.urls import path
from django.contrib.auth.views import LoginView
from .views import new_author, BaseRegisterView

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    path('newauthor/', new_author, name='new_author'),
    path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
]