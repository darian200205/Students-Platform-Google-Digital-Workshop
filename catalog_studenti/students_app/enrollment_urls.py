from django.urls import path
from catalog_studenti.students_app.enrollment_services import enrollment_views

urlpatterns = [
    path('list/', enrollment_views.enrollment_list, name='enrollment_list'),
    path('create_enrollment/', enrollment_views.create_enrollment, name='create_enrollment'),
    path('update_enrollment/<int:pk>/', enrollment_views.update_enrollment, name='update_enrollment'),
    path('delete_enrollment/<int:pk>/', enrollment_views.delete_enrollment, name='delete_enrollment'),
    path('grade_enrollment/<int:pk>/', enrollment_views.grade_enrollment, name='grade_enrollment'),
    path('delete_grade/<int:pk>/', enrollment_views.delete_grade, name='delete_grade')
]