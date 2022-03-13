from django.urls import path
from . import student_services
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', student_services.student_views.student_list, name='student_list'),
    path('profile/', student_services.student_views.student_profile, name='student_profile'),
    path('logout/', student_services.student_views.logout_student, name='student_logout'),
    path('register/', student_services.student_views.register_student, name='register_student'),
    path('login/', student_services.student_views.login_student, name='login_student'),
    path('create_student/', student_services.student_views.create_student, name='create_student'),
    path('update_student/<int:pk>/', student_services.student_views.update_student, name='update_student'),
    path('delete_student/<int:pk>/', student_services.student_views.delete_student, name='delete_student')
]