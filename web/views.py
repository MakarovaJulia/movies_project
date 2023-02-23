from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout


User = get_user_model()

def main_view(request):
    return render(request, "web/main.html")