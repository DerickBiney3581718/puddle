from django.urls import path
from .views import new_conversation, inbox, detail

app_name = 'conversation'

urlpatterns = [
    path('new/<int:pk>', new_conversation, name='new'),
    path('', inbox, name='inbox'),
    path('<int:pk>', detail, name='detail'),


]
