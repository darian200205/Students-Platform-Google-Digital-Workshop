from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.enrollment_list, name='enrollment_list'),
    path('create_enrollment/', views.create_enrollment, name='create_enrollment'),
    path('update_enrollment/<int:pk>/', views.update_enrollment, name='update_enrollment'),
    path('delete_enrollment/<int:pk>/', views.delete_enrollment, name='delete_enrollment'),
    path('grade_enrollment/<int:pk>/', views.grade_enrollment, name='grade_enrollment'),
    path('delete_grade/<int:pk>/', views.delete_grade, name='delete_grade')
]