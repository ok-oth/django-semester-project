from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('signup/', views.signup, name='signup'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
]