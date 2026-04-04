from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)
    class Meta:
       model = Post
       fields = ['author','title','content','category']
