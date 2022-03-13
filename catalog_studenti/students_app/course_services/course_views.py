from django.shortcuts import render, redirect

from ..models import Subject
from ..forms import SubjectForm, EnrollmentForm

from ..decorators import allowed_users


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
        "course_templates\subject_list.html",
        {
            "subjects": subjects,
            "student_courses": student_courses,
            "group": group
        }
    )


@allowed_users(allowed_roles=['teachers'])
def create_subject(request):
    form = SubjectForm()

    if request.method == "POST":
        subject = SubjectForm(request.POST)
        if subject.is_valid():
            subject.save()
            return redirect('/subject/list')

    context = {'form': form}
    return render(request, 'course_templates\subject_form.html', context)


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
    return render(request, 'course_templates\subject_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)

    if request.method == "POST":
        subject.delete()
        return redirect('/subject/list')

    return render(request)


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
    return render(request, 'course_templates\subject_list.html')