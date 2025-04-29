from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from itertools import groupby
from django.urls import reverse
from django.db.models.aggregates import Avg, Sum, Count, Min, Max

# Create your views here.

def apresentation(request):
    return render(request, 'index.html')

