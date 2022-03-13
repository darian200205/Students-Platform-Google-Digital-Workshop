from django.shortcuts import render, redirect

from ..models import CourseEnrollment
from ..forms import EnrollmentForm, GradeForm

from django.core.paginator import EmptyPage, Paginator

from ..decorators import allowed_users


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
        "enrollment_templates\enrollment_list.html",
        {
            "enrollments": page,
            "number_of_pages": number_of_pages
        }
    )


@allowed_users(allowed_roles=['teachers'])
def create_enrollment(request):
    form = EnrollmentForm()
    if request.method == "POST":
        enrollment = EnrollmentForm(request.POST)
        if enrollment.is_valid():
            enrollment.save()
            return redirect('/enrollment/list')

    return render(request, 'enrollment_templates\enrollment_form.html', context={
        'form': form
    })


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
    return render(request, 'enrollment_templates\enrollment_form.html', context)


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
    return render(request, 'enrollment_templates\grade_form.html', context)


@allowed_users(allowed_roles=['teachers'])
def delete_grade(request, pk):
    enrollment = CourseEnrollment.objects.get(id=pk)
    form = GradeForm()

    if request.method == "POST":
        if enrollment.grades_list:
            enrollment.grades_list = enrollment.grades_list[:-2]

        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect("/enrollment/list/")

    return render(request)