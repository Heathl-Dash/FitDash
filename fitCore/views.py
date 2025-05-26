from django.shortcuts import render,HttpResponse


def first(request):
    return HttpResponse('FitDash Init')