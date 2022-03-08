from django.db import models
from django.conf import settings
from django.core.validators import int_list_validator, validate_comma_separated_integer_list
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.forms import User
from django.contrib.auth.backends import ModelBackend, BaseBackend


class Student(models.Model):
    class Meta:
        db_table = "students"

    YEAR_CHOICES = (
        ("1", "YEAR 1"),
        ("2", "YEAR 2"),
        ("3", "YEAR 3"),
        ("0", "TEACHER")
    )

    full_name = models.CharField(max_length=30, blank=False, null=False)

    year = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES,
        blank=False,
        null=False
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.full_name)


class Subject(models.Model):
    class Meta:
        db_table = "subjects"

    course_name = models.CharField(max_length=30)
    students = models.ManyToManyField(Student, through='CourseEnrollment', null=True, blank=True)

    def __str__(self):
        return self.course_name

    def get_students_count(self):
        return self.students.count()

    def get_students(self):
        my_students = self.students.all()
        if self.get_students_count() > 4:
            my_students = my_students[:4]
            my_str = ', '.join([str(student) for student in my_students])
            my_str += f" si inca {self.students.count() - 4}"
        else:
            my_str = ', '.join([str(student) for student in my_students])
        return my_str


class CourseEnrollment(models.Model):
    class Meta:
        db_table = 'enrollments'

    GRADE_CHOICES = (
        ("10", "10"),
        ("9", "9"),
        ("8", "8"),
        ("7", "7"),
        ("6", "6"),
        ("5", "5"),
        ("4", "4"),
        ("3", "3"),
        ("2", "2"),
        ("1", "1"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grades = models.CharField(
        validators=[int_list_validator],
        max_length=30,
        blank=True,
        null=True,
        choices=GRADE_CHOICES
    )

    grades_list = models.CharField(
        validators=[int_list_validator],
        max_length=30,
        blank=True,
        null=True,
    )

    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['student', 'subject']]

    def __str__(self):
        return f'Student {self.student} enrolled at {self.subject}'

class Settings(models.Model):
     is_teacher = models.BooleanField()
