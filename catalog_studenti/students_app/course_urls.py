from django.urls import path
from .course_services import course_views

urlpatterns = [
    path('list/', course_views.subject_list, name='subject_list'),
    path('create_subject/', course_views.create_subject, name='create_subject'),
    path('update_subject/<int:pk>/', course_views.update_subject, name='update_subject'),
    path('delete_subject/<int:pk>/', course_views.delete_subject, name='delete_subject'),
    path('enroll_student/<int:pk>/', course_views.enroll_student, name='enroll_student')
]