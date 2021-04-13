from django import forms

from post.models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body','image','videofile']

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body','image','videofile']

    def save(self,commit=True):
        post=self.instance
        post.title=self.cleaned_data['title']
        if self.cleaned_data['body']:
            post.body=self.cleaned_data['body']

        if self.cleaned_data['image']:
            post.image=self.cleaned_data['image']

        if self.cleaned_data['videofile']:
            post.videofile=self.cleaned_data['videofile']

        if commit:
            post.save()
        return post