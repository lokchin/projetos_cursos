from django.shortcuts import render, get_list_or_404
from django.template import loader
from django.http import HttpResponse, Http404    
from .models import Questao


def index(request):
    lista_ultima_questao = Questao.objects.order_by('-data_publi')[:5]
    contexto = {"lista_ultima_questao": lista_ultima_questao,}
    return render(request, "polls/index.html", contexto)

def detalhe(request, idquestao):
    questao = get_list_or_404(Questao, pk=idquestao)
    return render(request, "polls/detalhe.html", {"questao": questao})

def resultado(request, idquestao):
    resposta = "Resultado da questão: %s"
    return HttpResponse(resposta % idquestao)

def voto(request, idquestao):
    return HttpResponse("Votou na questão %s" % idquestao)