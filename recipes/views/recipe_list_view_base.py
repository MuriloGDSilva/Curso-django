
from django.http import Http404
from recipes.models import Recipe, Category
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
from django.db.models import Q
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase,):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id'),
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        category_id = self.kwargs.get('category_id')
        category = Category.objects.get(id=category_id)

        context.update(
            {'title': category.name}
        )
        return context


class RecipeListViewSearch(RecipeListViewBase,):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q', )

        if not search_term:
            raise Http404()

        querry_set = super().get_queryset()
        querry_set = querry_set.filter(
            Q(
                Q(title__icontains=search_term,) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        )

        return querry_set

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', )
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })

        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context = context.update({
            'is_detail_page': True
        })

        return context
