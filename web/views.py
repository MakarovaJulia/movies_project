from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.forms import RegistrationForm, AuthForm, MovieForm, MovieGenreForm
from web.models import Movie, MovieGenre

User = get_user_model()


def main_view(request):
    movies = Movie.objects.all()
    return render(request, "web/main.html",
                  {
                      'movies': movies
                  })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('main')


def movies_edit_view(request, id=None):
    movie = Movie.objects.get(id=id) if id is not None else None
    form = MovieForm(instance=movie)
    if request.method == 'POST':
        form = MovieForm(data=request.POST, files=request.FILES, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/movies_form.html", {"form": form})


def genres_view(request):
    return _list_editor_view(request, MovieGenre, MovieGenreForm, "genres", "genres")


def genre_delete_view(request, id):
    genre = MovieGenre.objects.get(id=id)
    genre.delete()
    return redirect('genres')


def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.filter(user=request.user)
    form = form_cls()
    if request.method == 'POST':
        form = form_cls(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect(url_name)
    return render(request, f"web/{template_name}.html", {"items": items, "form": form})