from django.urls import path,include
from . import views

urlpatterns = [
    path('list/', views.subject_list, name='subject_list'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('update_subject/<int:pk>/', views.update_subject, name='update_subject'),
    path('delete_subject/<int:pk>/', views.delete_subject, name='delete_subject'),
]