from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest


def health_check(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("OK", content_type="text/plain", status=200)


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "50x.html", status=500)
