from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from . import getword


def engtool(request):
    try:
        word = request.GET.get('word')
        print(word)
        result = getword.getWord(word)
    except TypeError:
        raise Http404
    return HttpResponse(result)


def index(request):
    return HttpResponseRedirect('https://www.mrxzh.com/')