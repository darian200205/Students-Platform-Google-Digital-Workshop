from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Student
from django.contrib.auth import authenticate, login, logout


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == "teachers":
                return redirect('/student/list')
            else:
                return redirect('/student/profile')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                if group == 'teachers':
                    return HttpResponse("You are not a student")
                else:
                    return HttpResponse("You are not a teacher")

        return wrapper

    return decorator
