from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('records:login')  # Redirect to login page if user is not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper

def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.groups.filter(name=group_name).exists():
                return redirect('login')  # Redirect to login page or access denied page
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator