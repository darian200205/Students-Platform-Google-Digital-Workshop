from django.shortcuts import render, redirect

from .forms import StudentForm
from .models import Subject, Student, CourseEnrollment
from .forms import StudentForm, SubjectForm, EnrollmentForm, GradeForm


# Create your views here.


def student_list(request):
    students_list = Student.objects.all()
    # grades_list = Grade.objects.all()

    return render(
        request,
        "student_list.html",
        {
            "students": students_list,
        }
    )


def subject_list(request):
    subjects_list = Subject.objects.all()
    

    return render(
        request,
        "subject_list.html",
        {
            "subjects": subjects_list,
           
        }
    )


def enrollment_list(request):
    enrollments_list = CourseEnrollment.objects.all()

    return render(
        request,
        "enrollment_list.html",
        {
            "enrollments": enrollments_list
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
    form = StudentForm(instance=student)  #  uplem formul cu datele studentului

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

    if request.method == "POST":
        print(enrollment.grades_list)
        if enrollment.grades_list:
            enrollment.grades_list = enrollment.grades_list[:-2]

        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('/enrollment/list')
    
    return render(request)

