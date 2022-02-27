from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import StudentForm
from .models import Subject, Student, CourseEnrollment
from .forms import StudentForm, SubjectForm, EnrollmentForm, GradeForm, CreateUserForm, LoginUserForm

from django.core.paginator import EmptyPage, Paginator

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users


@login_required(login_url='/student/login')
@allowed_users(allowed_roles=['admin'])
def student_list(request):
    students_list = Student.objects.all()

    # grades_list = Grade.objects.all()
    p = Paginator(students_list, 6)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    number_of_pages = p.num_pages

    return render(
        request,
        "student_list.html",
        {
            "students": page,
            "number_of_pages": number_of_pages
        }
    )


def subject_list(request):
    subjects_list = Subject.objects.all()

    p = Paginator(subjects_list, 20)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    number_of_pages = p.num_pages

    return render(
        request,
        "subject_list.html",
        {
            "subjects": page,
            "number_of_pages": number_of_pages
        }
    )


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
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        student_form = StudentForm(request.POST)
        if form.is_valid() and student_form.is_valid():
            form.instance.username = request.POST['email']

            new_user = form.save()
            student = student_form.save(commit=False)

            if student.user_id is None:
                student.user_id = new_user.id

            student.save()
            login(request, new_user)
            return redirect('/student/profile')
            # messages.success(request, 'Your student account was created successfully')
    context = {
        'form': form,
        'student_form': student_form
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
            login(request, user)
            return redirect('/student/profile')

        else:
            messages.info(request, "Username or password incorrect", )
            return redirect('/student/login')

    context = {'login_form': login_form}
    return render(request, 'registration\student_login.html', context)


def logout_student(request):
    logout(request)
    return redirect('/student/login')


@login_required(login_url='/student/login')
def student_profile(request):
    if request.user.is_authenticated:
        student = request.user.student
        courses = student.subject_set.all()
        number_of_courses = student.subject_set.count()

        context = {
            'student': student,
            'courses': courses,
            'number_of_courses': number_of_courses
        }
        return render(request, 'student_profile.html', context)

    else:
        return redirect('/student/login')


def create_subject(request):
    form = SubjectForm()

    if request.method == "POST":
        subject = SubjectForm(request.POST)
        if subject.is_valid():
            subject.save()
            return redirect('/subject/list')

    context = {'form': form}
    return render(request, 'subject_form.html', context)


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


def delete_student(request, pk):
    student = Student.objects.get(id=pk)

    if request.method == "POST":
        student.delete()
        return redirect('/student/list')

    return render(request, '/student/list')


def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        subject.delete()
        return redirect('/subject/list')

    return render(request)


def delete_enrollment(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)

    if request.method == "POST":
        enrollment.delete()
        return redirect('/enrollment/list')

    return render(request)


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
