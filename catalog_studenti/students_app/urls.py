from django.urls import path,include
from . import views

urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('profile/', views.student_profile, name='student_profile'),
    path('logout/', views.logout_student, name='student_logout'),
    path('register/', views.register_student, name='register_student'),
    path('login/', views.login_student, name='login_student'),
    path('create_student/', views.create_student, name='create_student'),
    path('update_student/<int:pk>/', views.update_student, name='update_student'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student')
]