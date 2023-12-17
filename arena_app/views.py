from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Case, When, IntegerField
from .forms import UserLoginForm, UserRegistrationForm
from .forms import BettingTipForm
from .models import UserProfile


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
    # Query to get top tipsters for each category
    overall_tipsters = UserProfile.objects.annotate(
        total_bets=Count('tip'),
        total_wins_count=Sum(Case(When(tip__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    football_tipsters = UserProfile.objects.filter(
        tip__sport__name="Football"
    ).annotate(
        total_bets=Count('tip'),
        total_wins_count=Sum(Case(When(tip__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    # Similar queries for other sports
    racing_tipsters = UserProfile.objects.filter(
        tip__sport__name="Horse Racing"
    ).annotate(
        total_bets=Count('tip'),
        total_wins_count=Sum(Case(When(tip__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    tennis_tipsters = UserProfile.objects.filter(
        tip__sport__name="Tennis"
    ).annotate(
        total_bets=Count('tip'),
        total_wins_count=Sum(Case(When(tip__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    golf_tipsters = UserProfile.objects.filter(
        tip__sport__name="Golf"
    ).annotate(
        total_bets=Count('tip'),
        total_wins_count=Sum(Case(When(tip__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    context = {
        'overall_tipsters': overall_tipsters,
        'football_tipsters': football_tipsters,
        'racing_tipsters': racing_tipsters,
        'tennis_tipsters': tennis_tipsters,
        'golf_tipsters': golf_tipsters,
    }
    return render(request, 'tipster-league-table.html', context)


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
            return redirect('signin')
        # Assuming 'signin' is the name of your login URL.
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
def submit_tips(request):
    # Retrieve the user's current points balance
    user_profile = get_object_or_404(UserProfile,
                                     username=request.user.username)
    user_points_balance = user_profile.points_balance
    # Replace with actual field name for points balance

    if request.method == 'POST':
        form = BettingTipForm(request.POST,
                              initial={'user_points_balance': user_points_balance})
        if form.is_valid():
            # Check if the points bet exceeds user's balance
            points_bet = form.cleaned_data['points_bet']
            if points_bet > user_points_balance:
                form.add_error('points_bet',
                               'You cannot bet more points than your current balance.')
            else:
                # Create a new Tip instance but don't save it to the database yet
                new_tip = form.save(commit=False)
                new_tip.user = request.user
                new_tip.sport = form.cleaned_data['sport']
                new_tip.bet_description = form.cleaned_data['bet_description']
                new_tip.reasoning = form.cleaned_data['reasoning']
                new_tip.odds_given = form.cleaned_data['odds_given']
                new_tip.points_bet = points_bet

                # Update user's points balance
                user_profile.points_balance -= points_bet
                user_profile.save()

                new_tip.save()  # Save the tip to the database
                return redirect('submission_success')  # Redirect to a success page
    else:
        form = BettingTipForm(initial={'user_points_balance': user_points_balance})

    return render(request, 'submit_tips.html', {'form': form,
                                                'points_balance': user_points_balance})


def submission_success(request):
    return render(request, 'submission_success.html')
