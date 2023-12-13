from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm
from .models import Fixture, Tip
from .forms import BettingTipForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')


@login_required
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def football(request):
    return render(request, 'football.html')


def horse_racing(request):
    return render(request, 'horse_racing.html')


def tennis(request):
    return render(request, 'tennis.html')


def golf(request):
    return render(request, 'golf.html')


def tipster_league_table(request):
    return render(request, 'tipster_league_table.html')


def latest_tips(request):
    return render(request, 'latest_tips.html')


def general_chat(request):
    return render(request, 'general_chat.html')


def fixtures_results(request):
    return render(request, 'fixtures_results.html')


def in_play(request):
    return render(request, 'inplay.html')


def terms_of_service(request):
    return render(request, 'termsofservice.html')


def contact(request):
    return render(request, 'contact.html')


def privacy_policy(request):
    return render(request, 'privacypolicy.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page.
            return redirect('signin')  # Assuming 'signin' is the name of your login URL.
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def signin(request):
    # Redirect authenticated users to the home page
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print("Authenticated user:", user)  # Debugging line

            if user is not None:
                login(request, user)
                return redirect('home')  # Adjust the URL as needed
            else:
                # If authentication fails, add an error message
                messages.error(request, 'Invalid username or password.')
                print("Authentication failed")  # Debugging line

        else:
            # If form is not valid, add form errors as messages
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('index')  # Redirect login page

@login_required
def submit_football_tip(request):
    if request.method == 'POST':
        form = BettingTipForm(request.POST)
        if form.is_valid():
            # Create a new Tip instance but don't save it to the database yet
            new_tip = form.save(commit=False)
            new_tip.user = request.user  # Assign the current user to the tip
            
            # Handle additional fields
            new_tip.home_team_odds = form.cleaned_data['home_team_odds']
            new_tip.draw_odds = form.cleaned_data['draw_odds']
            new_tip.away_team_odds = form.cleaned_data['away_team_odds']
            # Handle any other additional fields as needed
            
            new_tip.save()  # Save the tip to the database
            return redirect('submission_success')  # Redirect to a success page or another appropriate page
    else:
        form = BettingTipForm()  # Create a new form instance for a GET request
        fixtures = Fixture.objects.all()
    return render(request, 'football_tips.html', {'form': form, 'fixtures': fixtures})


def submission_success(request):
    return render(request, 'submission_success.html')

