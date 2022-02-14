from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout
from django import forms
from .models import Student, Subject, CourseEnrollment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from crispy_forms.helper import FormHelper as helper

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        labels = {
            'full_name': 'Nume de familie si prenume',
            'year': 'Anul'
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['course_name']
        labels = {
            'course_name': 'Numele cursului',
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['student', 'subject']
        labels = {
            'student': 'Studentul',
            'subject': 'Cursul',
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['grades']
        labels = {
            'grades': 'Nota'
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['email', 'full_name', 'year', 'password1', 'password2']
