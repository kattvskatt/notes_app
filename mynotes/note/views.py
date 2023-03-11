from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *


class NotesHome(DataMixin, ListView):
    model = Notes
    template_name = 'note/index.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title='Мои заметки')
        return context | context_extra

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user.id)

class NotesCategory(DataMixin, ListView):
    model = Notes
    template_name = 'note/index.html'
    context_object_name = 'notes'
    allow_empty = False

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user.id, category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title='Категория - ' + str(context['notes'][0].category),
                                              cat_selected=context['notes'][0].category_id)
        return context | context_extra

class ShowNote(DataMixin, DetailView):
    model = Notes
    template_name = 'note/spec_note.html'
    slug_url_kwarg = 'note_slug'
    context_object_name = 'note'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title=context['note'])
        return context | context_extra

class AddNote(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddNoteForm
    template_name = 'note/add_note.html'
    # login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title='Добавление заметки')
        return context | context_extra

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return redirect('home')

class UpdateNote(DataMixin, UpdateView):
    model = Notes
    slug_url_kwarg = 'note_slug'
    form_class = EditNoteForm
    context_object_name = 'note'
    template_name = 'note/edit_note.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title=f'Редактирование заметки «{context["note"].title}»')
        return context | context_extra

class DeleteNote(DeleteView):
    model = Notes
    template_name = 'note/confirm_deletion.html'
    slug_url_kwarg = 'note_slug'
    context_object_name = 'note'

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'note/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title='Регистрация')
        return context | context_extra

    def form_valid(self, form):
        user = form.save()
        Notes.objects.create(
            title='Новая заметка',
            slug=f'{user}-new-note',
            content='Текст заметки...',
            category_id='5',
            user_id=user.pk
        )
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'note/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_user_context(title='Авторизация')
        return context | context_extra

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




