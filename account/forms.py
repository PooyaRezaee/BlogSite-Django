from django import forms
from .models import User

class RegisterUserForm(forms.Form):
    AVATAR_CHOICES = (
        (1, 'Man1'),
        (2, 'Man2'),
        (3, 'Woman1'),
        (4, 'Woman2'),
    )

    avatar = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter UserName'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter FirstName'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter LastName'}))


class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}))

class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ("first_name","last_name","bio","avatar","username","email")

class CreatePostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    thumbnail = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}),required=False)