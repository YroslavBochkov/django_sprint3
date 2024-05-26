from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404

from .models import Post, Category

NUM_POSTS_TO_DISPLAY = 5


def get_posts(post_objects):
    """Фильтрация постов."""
    return post_objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    ).prefetch_related('category')


def index(request):
    """Отображение последних NUM_POSTS_TO_DISPLAY постов."""
    template = 'blog/index.html'
    post_list = get_posts(Post.objects)[:NUM_POSTS_TO_DISPLAY]

    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    """Отображение деталей конкретного поста."""
    template = 'blog/detail.html'
    try:
        post = Post.objects.get(
            id=post_id,
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )
    except Post.DoesNotExist:
        raise Http404("Пост не существует или не опубликован.")
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Отображение всех постов в конкретной категории."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = get_posts(Post.objects.filter(category=category))
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
