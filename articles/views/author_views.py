from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.model import get_user_model
from ..models import Author
from ..forms import AuthorForm

class AuthorCreateView(CreateView):
    model = Author
    template_name = 'authors/create.html'
    form_class = AuthorForm
    success_url = reverse_lazy('author_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = reverse('author_create')
        return context


class AuthorListView(ListView):
    template_name = 'author/list.html'
    model = get_user_model()
    context_object_key = 'users'
    paginate_by = 5
    paginate_orphans = 1


class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'authors/update.html'
    form_class = AuthorForm
    success_url = reverse_lazy('author_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = reverse('author_update', kwargs={'pk': self.kwargs.get('pk')})
        return context
    
class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)