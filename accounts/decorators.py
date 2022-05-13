"""
This script shows the helper functions the view
for all the functions, by using @function_name in the views.py,
the view function can understand which authentication limit 
the functiion is used

For detial useage, please check view.py
"""
from django.http import HttpResponse
from django.shortcuts import redirect

"""
Determine that the decorated function is shown to
visitors that haven't log in yet
"""
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('Profile')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


"""
Determine that the decorated function is shown to
visitors that are valid users
"""
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

"""
Determine that the decorated function is shown to
visitors that are administrative users
"""
def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function