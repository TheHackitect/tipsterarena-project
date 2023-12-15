# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import Tip 


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Tip


class BettingTipForm(forms.ModelForm):
    # Dropdown for sport selection
    SPORT_CHOICES = [
        ('Football', 'Football'),
        ('Golf', 'Golf'),
        ('Horse Racing', 'Horse Racing'),
        ('Tennis', 'Tennis'),
    ]
    sport = forms.ChoiceField(choices=SPORT_CHOICES)

    # Textarea for bet description
    bet_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'maxlength': 250}),
        label="Bet Description"
    )

    # Optional textarea for reasoning
    reasoning = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'maxlength': 1000}),
        required=False,
        label="Reasoning (Optional)"
    )

    # Input for the odds
    odds_given = forms.DecimalField(
        max_digits=5, 
        decimal_places=2,
        label="Odds"
    )

    class Meta:
        model = Tip
        fields = ['sport', 'bet_description', 'reasoning', 'odds_given']
