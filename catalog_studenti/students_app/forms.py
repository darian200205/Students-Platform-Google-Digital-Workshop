from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout
from django import forms
from .models import Student, Subject, CourseEnrollment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserModel, User
from django.contrib.auth.forms import AuthenticationForm


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'year']
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
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        if User.objects.get(email=cleaned_email) is not None:
            raise forms.ValidationError("There is already an account with the entered email!")
        return cleaned_email


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        labels = {
            'email': 'Email'
        }
