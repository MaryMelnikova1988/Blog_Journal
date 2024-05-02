from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import RegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Валидная форма регистрации пользователя"""
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect('users:verify_message')

    def get_success_url(self):
        """Получение URL для перенаправления после успешной регистрации"""
        return reverse('users:verify_message')


class ProfileView(UpdateView):
    """Профиль пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:success_message')

    def get_object(self, queryset=None):  # тем самым уходим от привязки с pk
        return self.request.user
