from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:pk>/', views.edit_assignment, name='edit_assignment'),
    path('delete/<int:pk>/', views.delete_assignment, name='delete_assignment'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
]