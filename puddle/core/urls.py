from django.urls import path
from .views import contact, index, signup
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('', index, name='index'),
    path('signup/', signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name = 'core/login.html'), name="login")

]
