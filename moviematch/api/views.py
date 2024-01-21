from django.shortcuts import render
# In your Django views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



@csrf_exempt
def register_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        try:
            validate_email(username)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format"}, status=400)
        name = data.get('name')
        password = data.get('password')

        # Additional validations can be added here

        try:
            user = User.objects.create_user(username=username, name=name, password=password)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"message": "User created successfully"}, status=201)
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)

