from django.shortcuts import render
from django.http import HttpResponse
from .models import Categories

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    dict_cat = {
        'category': Categories.objects.all()
    }
    return render(request, 'about.html', dict_cat)

def booking(request):
    return render(request, 'booking.html')

def places(request):
    return render(request, 'places.html')

def contact(request):
    return render(request, 'contact.html')
    