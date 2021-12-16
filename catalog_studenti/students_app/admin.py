from django.contrib import admin

# Register your models here.

from .models import Student, Subject, CourseEnrollment

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(CourseEnrollment)
