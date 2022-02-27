from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/student/profile')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    pass


"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
             group = None
             if request.users.groups.exists():
                 pass
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
"""
