from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import User, Medication
from django.forms import TextInput, Textarea, NumberInput


class LoginForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password1', 'password2', 'admin', 'patient')


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = [
            'name', 'description', 'price', 'stock_quantity'
        ]

        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 330px',
                'placeholder': 'Name of Medicine'
            }),

            'stock_quantity': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 330px',
                'placeholder': 'Stock qunatity'
            }),
            'price': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 330px',
                'placeholder': 'Price'
            }),
            'description': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 94%',
                'placeholder': 'Description'
            }),
        }