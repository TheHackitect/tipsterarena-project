from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm

# Create your views here.
def index(request):
    return redirect(request, 'home/')
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
    return render(request, 'register.html')



def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Adjust the URL as needed

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')  # Redirect to home or login page