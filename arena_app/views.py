from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Case, When, IntegerField
from .forms import UserLoginForm, UserRegistrationForm
from .forms import BettingTipForm
from .models import UserProfile, TipsterStats, Sport, Tip


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
        total_bets=Count('tips'),
        total_wins_count=Sum(Case(When(tips__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    football_tipsters = UserProfile.objects.filter(
        tips__sport__name="Football"
    ).annotate(
        total_bets=Count('tips'),
        total_wins_count=Sum(Case(When(tips__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    # Similar queries for other sports
    racing_tipsters = UserProfile.objects.filter(
        tips__sport__name="Horse Racing"
    ).annotate(
        total_bets=Count('tips'),
        total_wins_count=Sum(Case(When(tips__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    tennis_tipsters = UserProfile.objects.filter(
        tips__sport__name="Tennis"
    ).annotate(
        total_bets=Count('tips'),
        total_wins_count=Sum(Case(When(tips__is_win=True, then=1), default=0,
                             output_field=IntegerField())),
    ).order_by('-points_balance')[:100]

    golf_tipsters = UserProfile.objects.filter(
        tips__sport__name="Golf"
    ).annotate(
        total_bets=Count('tips'),
        total_wins_count=Sum(Case(When(tips__is_win=True, then=1), default=0,
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
    # Fetch the latest tips, you can adjust the number of tips and ordering as needed
    latest_tips = Tip.objects.all().order_by('-created_at')[:100]  # Adjust as needed
    return render(request, 'latest-tips.html', {'latest_tips': latest_tips})



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
            user = form.save()
      
            # Create a TipsterStats instance for the registered user
            tipster_stats = TipsterStats.objects.create(user=user)
            
            # Debugging statements
            print("User registered:", user)
            print("TipsterStats created:", tipster_stats)
        
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
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        print("User is not authenticated")  # Add a print statement for debugging
        return redirect('signin')
    # Retrieve the user's current points balance
    user_profile = get_object_or_404(UserProfile, username=request.user.username)
    # Check if the user has tipster stats, create if not exist
    user_tipster_stats, _ = TipsterStats.objects.get_or_create(user=user_profile)
    
    user_points_balance = user_tipster_stats.points_balance
    # Replace with actual field name for points balance

    if request.method == 'POST':
        form = BettingTipForm(request.POST)
        if form.is_valid():
            sport_name = form.cleaned_data.get('sport')
            try:
                sport_instance = Sport.objects.get(name=sport_name)
            except Sport.DoesNotExist:
                form.add_error('sport', 'Invalid sport selected')
                return render(request, 'submit_tips.html', {'form': form})
            
            points_bet = form.cleaned_data.get('points_bet') 

            new_tip = form.save(commit=False)
            new_tip.user = request.user
            new_tip.sport = sport_instance
            new_tip.bet_description = form.cleaned_data['bet_description']
            new_tip.reasoning = form.cleaned_data['reasoning']
            new_tip.odds_given = form.cleaned_data['odds_given']
            new_tip.points_bet = ['points_bet']
        
            # Calculate points won
            points_won = user_tipster_stats.calculate_points_won(points_bet, new_tip.odds_given)

            # Update user's tipster stats
            user_tipster_stats.total_bets_placed += 1
            if new_tip.is_win:
                 user_tipster_stats.total_wins += 1

            # Save the user's tipster stats
            user_tipster_stats.save()

             # Update user's points balance (this might be done in the
             # calculate_points_won method)
            user_points_balance = user_tipster_stats.points_balance

            new_tip.save()  # Save the tip to the database
     
            # Display or use the points_won variable as needed
            messages.success(request, f'You won {points_won} points!')

            return redirect('submission_success')  # Redirect to a success page
    else:
        form = BettingTipForm(initial={'user_points_balance': user_points_balance})

    return render(request, 'submit_tips.html', {'form': form, 'points_balance': user_points_balance})


def submission_success(request):
    return render(request, 'submission_success.html')
