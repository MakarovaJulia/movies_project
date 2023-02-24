from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.forms import RegistrationForm, AuthForm, MovieForm, MovieGenreForm, MovieFilterForm
from web.models import Movie, MovieGenre

User = get_user_model()


@login_required
def main_view(request):
    movies = Movie.objects.filter(user=request.user).order_by('title')
    filter_form = MovieFilterForm(request.GET)
    filter_form.is_valid()
    filters = filter_form.cleaned_data

    if filters['search']:
        movies = movies.filter(title__icontains=filters['search'])

    if filters['release_date']:
        movies = movies.filter(release_date__gte=filters['release_date'])

    total_count = movies.count()
    movies = movies.prefetch_related("genres").select_related("user")

    page_number = request.GET.get("page", 1)
    paginator = Paginator(movies, per_page=10)

    return render(request, "web/main.html",
                  {
                      'movies': paginator.get_page(page_number),
                      'filter_form': filter_form,
                      'total_count': total_count
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


@login_required
def movies_edit_view(request, id=None):
    movie = get_object_or_404(Movie, user=request.user, id=id) if id is not None else None
    form = MovieForm(instance=movie)
    if request.method == 'POST':
        form = MovieForm(data=request.POST, files=request.FILES, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/movies_form.html", {"form": form})


@login_required
def movie_delete_view(request, id):
    movie = get_object_or_404(Movie, user=request.user, id=id)
    movie.delete()
    return redirect('main')


def genres_view(request):
    return _list_editor_view(request, MovieGenre, MovieGenreForm, "genres", "genres")


@login_required
def genre_delete_view(request, id):
    genre = get_object_or_404(MovieGenre, id=id)
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
