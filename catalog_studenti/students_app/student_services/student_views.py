from django.shortcuts import render, redirect
from django.contrib import messages

from ..models import Subject, Student, CourseEnrollment
from ..forms import StudentForm, EnrollmentForm, CreateUserForm, LoginUserForm, SettingsForm
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from ..decorators import unauthenticated_user, allowed_users


@login_required(login_url='/student/login')
@allowed_users(allowed_roles=['teachers'])
def student_list(request):
    students_list = Student.objects.all()

    return render(
        request,
        "student_templates\student_list.html",
        {
            "students": students_list
        }
    )


@allowed_users(allowed_roles=['teachers'])
def create_student(request):
    form = StudentForm()
    user_form = CreateUserForm()

    if request.method == "POST":
        form = StudentForm(request.POST)
        user_form = CreateUserForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            user_form.instance.username = request.POST['email']
            new_user = user_form.save()

            student = form.save(commit=False)

            if student.user_id is None:
                student.user_id = new_user.id

            student.save()
            group = Group.objects.get(name='students')
            group.user_set.add(new_user)

            return redirect('/student/list')

    context = {'form': form, 'user_form': user_form}
    return render(request, 'student_templates\student_form.html', context)


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
    enrollments = CourseEnrollment.objects.filter(student=student)

    context = {
        'student': student,
        'courses': courses,
        'number_of_courses': number_of_courses,
        'enrollments': enrollments
    }
    return render(request, 'student_templates\student_profile.html', context)


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
    return render(request, 'student_templates\subject_list.html')


@allowed_users(allowed_roles=['teachers'])
def update_student(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/student/list')

    context = {'form': form}
    return render(request, 'student_templates\student_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def delete_student(request, pk):
    student = Student.objects.get(id=pk)

    if request.method == "POST":
        student.user.delete()
        return redirect('/student/list')

    return render(request, 'student_templates\subject_list.html')
