from django.urls import path

from .views import *

urlpatterns = [
    path('', NotesHome.as_view(), name='home'), # home page
    path('addnote/', AddNote.as_view(), name='add_note'),
    path('edit/<slug:note_slug>/', UpdateNote.as_view(), name='edit_note'),
    path('delete/<slug:note_slug>/', DeleteNote.as_view(), name='delete_note'),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('note/<slug:note_slug>/', ShowNote.as_view(), name='note'),
    path('category/<slug:cat_slug>/', NotesCategory.as_view(), name='category'),
    ]