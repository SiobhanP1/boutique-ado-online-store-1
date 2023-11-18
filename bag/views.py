from django.shortcuts import render

# Create your views here.

def view_bag(request):
    """A view to show contents of shopping cart"""
    return render(request, 'bag/bag.html')