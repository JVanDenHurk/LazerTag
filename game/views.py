from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PlayerSignUpForm
from .models import Player
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            player = form.save()
            login(request, player)
            return redirect(reverse('leaderboard'))
        else:
            messages.error(request, "There was a problem with your signup. Please check the errors below.")
    else:
        form = PlayerSignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('leaderboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    return redirect('leaderboard')
                else:
                    messages.error(request, "Invalid username or password.")
            except ObjectDoesNotExist:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please provide both username and password.")
    return render(request, 'signin.html')

@login_required
def leaderboard(request):
    players = Player.objects.filter(is_active=True).order_by('-points')
    return render(request, 'leaderboard.html', {'players': players})

@login_required
def scan_qr(request, player_id):
    scanned_player = get_object_or_404(get_user_model(), id=player_id)
    player_profile = get_object_or_404(PlayerProfile, user=scanned_player)
    player_profile.kills += 1
    player_profile.save()
    return HttpResponse(f"{scanned_player.username} has been tagged!")

@login_required
def account(request):
    return render(request, 'account.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect(reverse('signup'))
    return render(request, 'delete_account_confirmation.html')

def signout(request):
    logout(request)
    return redirect('signin')