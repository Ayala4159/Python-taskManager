from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "email", "password", "role"]
        labels = {
            "last_name": "Last Name",
            "first_name": "First Name"
        }
        help_texts = {
            "last_name": "Should contains only letters",
            "first_name": "Should contains only letters",
            "password": "Min length of 8 characters",
            "email": "Email address",
            "role": "To open new teem- choose manger to join new teem-choose user"
        }

    def clean_first_name(self):
        firstName = self.cleaned_data["first_name"]
        if not firstName.isalpha():
            raise forms.ValidationError("Should contains only letters")
        return firstName

    def clean_last_name(self):
        lastName = self.cleaned_data["last_name"]
        if not lastName.isalpha():
            raise forms.ValidationError("Should contains only letters")
        return lastName
