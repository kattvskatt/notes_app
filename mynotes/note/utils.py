from django.db.models import Count, Q

from .models import Category

menu = [
        {'title': 'Добавить заметку', 'url_name': 'add_note'},
        # {'title': 'Войти', 'url_name': 'login'}
        ]

class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        # categories = Category.objects.all()
        categories = Category.objects.annotate(num_notes=Count('notes', filter=Q(notes__user=self.request.user.id)))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(0)  # вкладка "Добавить заметку" неавторизованным пользователям отображаться не будет
        context['menu'] = user_menu
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0  # Все категории
        return context