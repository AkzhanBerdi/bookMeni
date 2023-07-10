from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Author, Article

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',)

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label='Article name')

    class Meta:
        model = Article
        fields = ('title', 'author', 'body')

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'