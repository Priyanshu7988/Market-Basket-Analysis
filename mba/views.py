from django.shortcuts import render
from .ml_model import get_recommendations

def home(request):
    recommendations = None

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # IMPORTANT: pass file directly
        recommendations = get_recommendations(file)

    return render(request, 'home.html', {'recommendations': recommendations})