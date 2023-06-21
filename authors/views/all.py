from django.shortcuts import render, redirect
from authors.forms.recipe_dashboard_create_form import DashboardCreateRecipeForm
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe


def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login_view.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in. ')
            login(request, authenticated_user)

        else:
            messages.error(request, 'User do not exist')

    else:
        messages.error(request, 'Invalid credentials. ')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    logout(request)
    messages.success(request, 'user logged out successfully')
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html',
                  context={
                      'recipes': recipes,
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):

    form = DashboardCreateRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Your recipe has been created successfully')
        return redirect(reverse('authors:dashboard_recipe_edit',
                                kwargs={'id': recipe.id}))

    return render(request, 'authors/pages/dashboard_recipe_create.html',
                  context={
                      'form': form
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'Deleted successfully')
    return redirect(reverse('authors:dashboard'))