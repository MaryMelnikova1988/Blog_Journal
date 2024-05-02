import random

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blog.forms import BlogForm
from blog.models import Blog
from users.models import User


class BlogCreateView(CreateView):
    """Создание публикации"""
    model = Blog
    form_class = BlogForm
    # fields = ('title', 'body', 'preview', 'date_of_creation',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.author = self.request.user
            self.object.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """Получение листа публикаций"""
    model = Blog
    extra_context = {
        'title': " Блог",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user:
            queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Публикация в полном виде"""
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    """Редактирование публикации (только для автора)"""
    model = Blog
    form_class = BlogForm
    # fields = ('title', 'body', 'preview', 'date_of_creation',)
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Удаление публикации (только для автора)"""
    model = Blog
    success_url = reverse_lazy('blog:list')


def toogle_activity(request, pk):
    """Снять или опубликовать (только для автора)"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect('blog:list')


class IndexView(TemplateView):
    """Домашняя страница. Главная"""
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'Главная',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['publish_blog_count'] = len(Blog.objects.filter(is_published=True))
        context_data['users_count'] = len(User.objects.all())
        context_data['object_list'] = random.sample(list(Blog.objects.all()), 3)

        return context_data


def contacts(request):
    """Контакты. О нас"""
    context = {
        'title': "Контакты",
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name} ({phone}, {email}): {message}")

    return render(request, 'blog/contacts.html', context)