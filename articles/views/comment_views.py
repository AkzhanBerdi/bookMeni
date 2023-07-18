from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from ..forms import CommentForm
from ..helpers.views import CustomCreateView, CustomUpdateView, CustomDeleteView
from ..models import Article, Comment

class CommentCreateView(CustomCreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.get_article()
        return context

    def form_valid(self, form):
        form.instance.article = self.get_article()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_article(self):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return article

    def get_redirect_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

class CommentUpdateView(UserPassesTestMixin, CustomUpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm
    context_object_name = 'comment'
    
    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_redirect_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

class CommentDeleteView(UserPassesTestMixin, CustomDeleteView):
    model = Comment
    confirm_deletion = False
    context_object_name = 'comment'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_redirect_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.article.pk})