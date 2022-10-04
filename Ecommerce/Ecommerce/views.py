from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    # путь прописан в settings.py, templates DIR ('templates')