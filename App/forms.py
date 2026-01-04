from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User, Team


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "role"]
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

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("confirm_password")

        if pass1 and pass2 and pass1 != pass2:
            # זה יוצמד לשדה confirm_password ויוצג לידו אוטומטית
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

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

class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'email', 'password']
        help_texts = {
            "password": "min length of 8 characters",
            "email": "email address"}

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]
        labels = {'team_name': 'Create name for the team'}

class JoinTeamForm(forms.ModelForm):
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Select a team",
        empty_label="-- choose team to join --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['team']