from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .forms import StudentForm
from .models import Subject, Student, CourseEnrollment
from .forms import StudentForm, SubjectForm, EnrollmentForm, GradeForm, CreateUserForm, LoginUserForm, SettingsForm
from django.contrib.auth.models import Group

from django.core.paginator import EmptyPage, Paginator

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users


def home(request):
    return redirect('/student/register')


@login_required(login_url='/student/login')
@allowed_users(allowed_roles=['teachers'])
def student_list(request):
    students_list = Student.objects.all()

    return render(
        request,
        "student_list.html",
        {
            "students": students_list
        }
    )


@allowed_users(allowed_roles=['teachers', 'students'])
def subject_list(request):
    group = None
    group = request.user.groups.all()[0].name
    student_courses = None
    subjects = Subject.objects.all()
    if group == 'students':
        student_courses = request.user.student.subject_set.all()

    return render(
        request,
        "subject_list.html",
        {
            "subjects": subjects,
            "student_courses": student_courses
        }
    )


@allowed_users(allowed_roles=['teachers'])
def enrollment_list(request):
    enrollments_list = CourseEnrollment.objects.all()

    p = Paginator(enrollments_list, 5)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    number_of_pages = p.num_pages

    return render(
        request,
        "enrollment_list.html",
        {
            "enrollments": page,
            "number_of_pages": number_of_pages
        }
    )


@allowed_users(allowed_roles=['teachers'])
def create_student(request):
    form = StudentForm()

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/student/list')

    context = {'form': form}
    return render(request, 'student_form.html', context)


@unauthenticated_user
def register_student(request):
    form = CreateUserForm()
    student_form = StudentForm()
    is_teacher_form = SettingsForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        student_form = StudentForm(request.POST)
        is_teacher_form = SettingsForm(request.POST)

        if form.is_valid() and student_form.is_valid():
            form.instance.username = request.POST['email']
            answer = is_teacher_form.save()

            new_user = form.save()

            student = student_form.save(commit=False)

            if student.user_id is None:
                student.user_id = new_user.id

            student.save()

            login(request, new_user)

            if answer.is_teacher:
                new_user.is_staff = True
                group = Group.objects.get(name='teachers')
                group.user_set.add(new_user)
                return redirect('/student/list')

            group = Group.objects.get(name='students')
            group.user_set.add(new_user)
            return redirect('/student/profile')
            # messages.success(request, 'Your student account was created successfully')
    context = {
        'form': form,
        'student_form': student_form,
        'is_teacher_form': is_teacher_form
    }

    return render(request, 'registration\student_registration.html', context)


@unauthenticated_user
def login_student(request):
    login_form = LoginUserForm()
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name

            login(request, user)

            if group == 'students':
                return redirect('/student/profile')
            else:
                return redirect('/student/list')

        else:
            messages.info(request, "Username or password incorrect", )
            return redirect('/student/login')

    context = {'login_form': login_form}
    return render(request, 'registration\student_login.html', context)


def logout_student(request):
    logout(request)
    return redirect('/student/login')


@login_required(login_url='/student/login')
@allowed_users(allowed_roles=['students'])
def student_profile(request):
    student = request.user.student
    courses = student.subject_set.all()
    number_of_courses = student.subject_set.count()

    context = {
        'student': student,
        'courses': courses,
        'number_of_courses': number_of_courses
    }
    return render(request, 'student_profile.html', context)

    return redirect('/student/login')


@allowed_users(allowed_roles=['teachers'])
def create_subject(request):
    form = SubjectForm()

    if request.method == "POST":
        subject = SubjectForm(request.POST)
        if subject.is_valid():
            subject.save()
            return redirect('/subject/list')

    context = {'form': form}
    return render(request, 'subject_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def create_enrollment(request):
    form = EnrollmentForm()
    if request.method == "POST":
        enrollment = EnrollmentForm(request.POST)
        if enrollment.is_valid():
            enrollment.save()
            return redirect('/enrollment/list')

    return render(request, 'enrollment_form.html', context={
        'form': form
    })


def enroll_student(request, pk):
    course = Subject.objects.get(id=pk)
    context = {
        'student': request.user.student,
        'subject': course
    }
    enrollment = EnrollmentForm(context)
    if enrollment.is_valid():
        enrollment.save()
        return redirect('/subject/list')
    return render(request, 'subject_list.html')


@allowed_users(allowed_roles=['teachers'])
def update_student(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)  # uplem formul cu datele studentului

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/student/list')

    context = {'form': form}
    return render(request, 'student_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def update_subject(request, pk):
    subject = Subject.objects.get(id=pk)
    form = SubjectForm(instance=subject)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('/subject/list')

    context = {'form': form}
    return render(request, 'subject_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def update_enrollment(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)
    form = EnrollmentForm(instance=enrollment)

    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('/enrollment/list')

    context = {'form': form}
    return render(request, 'enrollment_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def delete_student(request, pk):
    student = Student.objects.get(id=pk)

    if request.method == "POST":
        student.delete()
        return redirect('/student/list')

    return render(request, '/student/list')


@allowed_users(allowed_roles=['teachers'])
def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        subject.delete()
        return redirect('/subject/list')

    return render(request)


@allowed_users(allowed_roles=['teachers'])
def delete_enrollment(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)

    if request.method == "POST":
        enrollment.delete()
        return redirect('/enrollment/list')

    return render(request)


@allowed_users(allowed_roles=['teachers'])
def grade_enrollment(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)
    form = GradeForm()

    if request.method == "POST":

        if enrollment.grades_list:
            enrollment.grades_list += " "
            enrollment.grades_list += request.POST['grades']

        else:
            enrollment.grades_list = request.POST['grades']

        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'grade_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def delete_grade(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)
    form = GradeForm()

    # page_number = request.GET.get('page', 1)
    # print("printing:-----", page_number)
    page_number = 2

    if request.method == "POST":
        print(enrollment.grades_list)
        if enrollment.grades_list:
            enrollment.grades_list = enrollment.grades_list[:-2]

        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect("/enrollment/list/")

    return render(request)
