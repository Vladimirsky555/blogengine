from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower() #self.cleaned.data.get('slug') - если обращаться из другой функции

        if new_slug == 'create':
            raise ValidationError('slug can not be Create')
        if Tag.objects.filter(slug__iexact=new_slug).count(): #если хоть что-то найдется
            raise ValidationError('ЧПУ для тэга должно быть уникальным! У нас уже есть "{}" тэг'.format(new_slug))
        return new_slug

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'tags']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs = {'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()  # self.cleaned.data.get('slug') - если обращаться из другой функции

            if new_slug == 'create':
                raise ValidationError('slug can not be Create')
            return new_slug





