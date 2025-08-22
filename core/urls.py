from django.urls import path
from .views import pessoas_list, pessoas_create, pessoas_edit, pessoas_delete

urlpatterns = [
    path("pessoas/", pessoas_list, name="pessoas_list"),
    path("pessoas/nova/", pessoas_create, name="pessoas_create"),
    path("pessoas/<int:pessoa_id>/editar/", pessoas_edit, name="pessoas_edit"),
    path("pessoas/<int:pessoa_id>/excluir/", pessoas_delete, name="pessoas_delete"),
]

