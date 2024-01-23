from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("idquestao/", views.detalhe, name="detalhe"),
    path("idquestao/resultado/", views.resultado, name="resultados"),
    path("idquestao/voto/", views.voto, name="voto"),
]