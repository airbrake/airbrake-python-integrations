# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from app.wtf import wtfDoBacktracesWork

# Create your views here.

from django.http import HttpResponse

def index(request):
    raise Exception("There is a nasty gremlin in this system")
    return HttpResponse("Hello, world. You're at the app index.")
