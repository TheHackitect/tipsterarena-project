# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import Tip


class UserRegistrationForm(UserCreationForm):
    """
    A form for user registration.

    Inherits from UserCreationForm and adds an email field.
    """

    email = forms.EmailField(required=True)

    class Meta:
        """
        The Meta class provides additional information about the form.
        It specifies the model to be used and the fields to be
        included in the form.
        """

        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the user registration form.

        Args:
            commit (bool, optional): Whether to save the user object
            to the database. Defaults to True.

        Returns:
            UserProfile: The saved user object.
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    A form for user login.

    This form includes fields for username and password.
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BettingTipForm(forms.ModelForm):
    """
    A form for creating a betting tip.

    This form allows users to create a betting tip by providing information
    such as the sport,
    bet description, reasoning (optional), odds, and the number of points
    to bet.

    Attributes:
        sport (ChoiceField): A dropdown field for selecting the sport.
        bet_description (CharField): A textarea field for entering the
        bet description.
        reasoning (CharField): An optional textarea field for providing
        reasoning behind the bet.
        odds_given (DecimalField): An input field for entering the odds.
        points_bet (IntegerField): An input field for entering the number of
        points to bet.

    Methods:
        clean_points_bet: Validates the number of points to bet against the
        user's points balance.

    """
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

    points_bet = forms.IntegerField(
        label="Enter Number of Points You Would Like To Bet Place",
        min_value=1,  # Minimum value for the bet
        widget=forms.NumberInput(attrs={'placeholder':
                                 'Enter Number of points to bet'})
    )

    class Meta:
        """
        The Meta class provides additional information about the TipForm class.
        It specifies the model to be used and the fields to be included
        in the form.
        """
        model = Tip
        fields = ['sport',
                  'bet_description',
                  'reasoning',
                  'odds_given',
                  'points_bet']

    def clean_points_bet(self):
        """
        Validates the number of points to bet against the user's
        points balance.

        Returns:
            int: The validated number of points to bet.

        Raises:
            forms.ValidationError: If the number of points to bet is greater
            than the user's points balance.
        """
        points_bet = self.cleaned_data['points_bet']
        user_points_balance = self.initial.get('user_points_balance', 1000)
        # Default to 1000 if not provided

        if points_bet > user_points_balance:
            raise forms.ValidationError("You cannot bet more points than your current balance.")

        return points_bet
