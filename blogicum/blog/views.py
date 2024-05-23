from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from.models import Post, Category


def get_posts(post_objects):
    """
    Фильтрация постов.
    """
    return post_objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """
    Отображение 5 последних опубликованных постов.
    """
    template = 'blog/index.html'
    post_list = get_posts(Post.objects).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    """
    Отображение деталей конкретного поста.
    """
    template = 'blog/detail.html'
    post = get_object_or_404(get_posts(Post.objects), id=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """
    Отображение всех постов в конкретной категории.
    """
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_posts(category.posts)
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
