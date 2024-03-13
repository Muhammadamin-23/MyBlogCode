from django import forms

from blog.models import Comment, ClientInfo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'message', ]
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Your name'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your comment here'}
            ),
        }


class ClientInfoForm(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = ['user', 'email', 'phone_number', 'message']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your comment here'}),
        }


from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
