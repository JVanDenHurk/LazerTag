from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PlayerSignUpForm
from .models import Player

def signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('leaderboard')
    else:
        form = PlayerSignUpForm()
    return render(request, 'game/signup.html', {'form': form})

@login_required
def leaderboard(request):
    players = Player.objects.filter(is_active=True).order_by('-points')
    return render(request, 'game/leaderboard.html', {'players': players})

def scan_qr(request, player_id):
    # Get the scanned player
    scanned_player = get_object_or_404(User, id=player_id)
    
    # Get or update the scanned player's profile (e.g., increase points or kills)
    player_profile = get_object_or_404(PlayerProfile, user=scanned_player)
    player_profile.kills += 1  # Increment kill count or points
    player_profile.save()
    
    # Optionally, return a success message or redirect to another page
    return HttpResponse(f"{scanned_player.username} has been tagged!")

def landing_page(request):
    return render(request, 'landing_page.html')

