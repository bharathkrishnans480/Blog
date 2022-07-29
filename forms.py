from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from blogapp.models import UserProfile,Blogs,Comments


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]
class LoginForm(forms.Form):
    username=forms.CharField(label='username')
    password=forms.CharField(label='password')

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','following',)

        widgets={
            'date_of_birth':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class ProfilePicForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            'profile_pic',
        ]

class BlogForm(ModelForm):
    class Meta:
        model=Blogs
        fields=[
            'title',
            'description',
            'image',
        ]
        widgets={
            "title":forms.TextInput(attrs={'class':'form-control'}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
        }
class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields=[
            "comment",
        ]
        wigdet={
            'comment':forms.TextInput(attrs={'class':'form-control'})
        }


