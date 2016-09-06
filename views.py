from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from .models import GameUser, GameUserData, Artist, ArtistData, Investment, Reward, GrammyEntry
from django.template.response import TemplateResponse
import pytz
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required()
def discover_featured_artists(request):
    featured_artists = Artist.objects.filter(is_featured=True)
    return TemplateResponse(request, 'game/discover_featured.html', {'artists': featured_artists})

@login_required()
def discover_artist(request, name):
    artist = Artist.objects.get(name=name)
    return TemplateResponse(request, 'game/discover_artist.html', {'media': artist})

@login_required()
def discover_all_artists(request):
    cur_user = GameUser.objects.get(user=request.user)
    artist_list = Artist.objects.all().order_by('price')
    return TemplateResponse(request, 'game/discover_all.html', {'game_user': cur_user, 'artist_list': artist_list})

@login_required()
def invest_in_artist(request, name):
    artist = Artist.objects.get(name=name)
    cur_user = GameUser.objects.get(user=request.user)
    investments = Investment.objects.all().filter(user=cur_user).filter(media=artist).exclude(shares=0)
    price_history = Data.objects.filter(media=artist).order_by('-date')[:7]
    cur_investment = None
    investment_processed = False
    if request.method == 'POST':
        shares_bought = int(request.POST['shares'])
        if shares_bought > 0:
            order_amount = artist.price * shares_bought
            cur_user.free_points -= order_amount
            if cur_user.free_points > 0:
                cur_user.invested_points += order_amount
                cur_investment = Investment(user=cur_user, media=artist, buy_price=artist.price, value=order_amount, shares=shares_bought)
                cur_user.save()
                cur_investment.save()
                investment_processed = True
    ui_slider_data = get_slider_positions(cur_user, artist)
    return TemplateResponse(request, 'game/invest2.html', {'media': artist, 'game_user': cur_user, 'investments': investments,
                                                           'ui_slider_data': ui_slider_data, 'investment_processed': investment_processed,
                                                           'price_history': price_history, 'cur_investment': cur_investment})

@login_required()
def sell_shares(request, trade_id):
    trade_info = Investment.objects.get(pk=trade_id)
    if trade_info.user.pk != GameUser.objects.get(user=request.user).pk:
        return render(request, 'game/500.html')
    artist = trade_info.media  # Artist.objects.get(pk=id)
    cur_user = trade_info.user  # GameUser.objects.get(user=request.user)
    sale_processed = False
    investments = Investment.objects.all().filter(user=cur_user).filter(media=artist).exclude(shares=0)
    price_history = Data.objects.filter(media=artist).order_by('-date')[:7]
    feedback_message = None
    transaction_amount, num_shares = 0
    if request.method == 'POST':
        num_shares = int(request.POST['shares'])
        sale_processed = True
        if num_shares < 1:
            feedback_message = "Something went wrong - you either didn't sell any shares or you tried to sell negative shares"
        else:
            transaction_amount = artist.price * num_shares
            cur_user.free_points += transaction_amount
            cur_user.invested_points -= transaction_amount
            trade_info.value -= num_shares * artist.price
            trade_info.shares -= num_shares
            if trade_info.shares < 0:
                feedback_message = "Something went wrong - try selling again!"
            else:
                trade_info.save()
                cur_user.save()
    ui_slider_data = get_slider_positions(cur_user, artist)
    return TemplateResponse(request, 'game/sell2.html', {'artist': artist, 'game_user': cur_user, 'trade': trade_info,
                                                         'investments': investments, 'ui_slider_data': ui_slider_data,
                                                         'sale_processed': sale_processed, 'price_history': price_history,
                                                         'feedback_message': feedback_message, 'transaction_amount': transaction_amount,
                                                         'num_shares': num_shares})

# computes values that need to be passed to the UI to set "amount-of-money-to-invest" picker to midpoint
def get_slider_positions(cur_user, artist):
    half_points = round(cur_user.free_points / 2, 2)
    half_shares = int(half_points / artist.price)
    max_shares = int(cur_user.free_points / artist.price)
    if max_shares < 1:
        max_shares = -99
    return (half_points, half_shares, max_shares)

@login_required()
def leaderboard(request):
    top_users = GameUser.objects.all().order_by('-points')[:75]
    cur_user = GameUser.objects.get(user=request.user)
    return TemplateResponse(request, 'game/leaderboard.html', {'top_users': top_users, 'game_user': cur_user})

@login_required()
def rewards(request):
    cur_user = GameUser.objects.get(user=request.user)
    rewards = Reward.objects.all()
    return TemplateResponse(request,'game/rewards.html', {'reward_list': rewards, 'game_user': cur_user})

def initialize_new_user(request):
    cur_user = GameUser(user=request.user, points=10000, invested_points=0, free_points=10000)
    cur_user.save()
    start_data = GameUserData(user=cur_user, points=10000, invested_points=0, free_points=10000)
    start_data.save()

@login_required()
def dashboard(request):
    if not GameUser.objects.filter(user=request.user).exists():  #detects if this is a new user
        initialize_new_user(request)
    if (datetime.now(pytz.utc) - request.user.date_joined).seconds < 30: #detects if the user joined less than 30 seconds ago
        return redirect('http://www.hiphoptycoon.com/tutorial')
    cur_user = GameUser.objects.get(user=request.user)
    game_user_history = GameUserData.objects.filter(user=cur_user).order_by('-date')[:7]
    recent_investments = Investment.objects.all().order_by('-buy_date')[:5]
    cur_time = datetime.now(pytz.utc)
    return TemplateResponse(request,'game/dashboard2.html',{'game_user_history': game_user_history, 'game_user': cur_user,
                                                            'recent_investments': recent_investments, 'now': cur_time})

@login_required()
def portfolio(request):
    cur_user = GameUser.objects.get(user=request.user)
    investments = Investment.objects.all().filter(user=cur_user).exclude(shares=0)
    artist_list = Artist.objects.all().order_by('price')
    return TemplateResponse(request, 'game/portfolio.html', {'game_user': cur_user, 'artist_list': artist_list, 'investments': investments})

@login_required()
def update_grammy_entries(request):
        all_entries = GrammyEntry.objects.all()
        return TemplateResponse(request,'game/grammy_entires.html', {'all_entries': all_entries})

def grammys(request):
    entry_feed = GrammyEntry.objects.all().order_by('-number_correct')[:125]
    cur_time = datetime.now(pytz.utc)
    error_message, cur_user, submitted_entry = None
    just_submitted = False
    if request.user.is_authenticated():
        cur_user = GameUser.objects.get(user=request.user)
        if GrammyEntry.objects.filter(user=cur_user).exists():
            submitted_entry = GrammyEntry.objects.get(user=cur_user)
        elif request.method == 'POST':
            if submitted_entry is not None:
                error_message = "You have already submitted once!"
            else:
                pick1 = request.POST['group1']
                pick2 = request.POST['group2']
                pick3 = request.POST['group3']
                pick4 = request.POST['group4']
                pick5 = request.POST['group5']
                cur_grammy_entry = GrammyEntry(user=cur_user, choice1=pick1, choice2=pick2, choice3=pick3, choice4=pick4,
                                               choice5=pick5, number_correct=0)
                cur_grammy_entry.save()
    return TemplateResponse(request,'game/grammys.html', {'error_message': error_message, 'submitted_entry': submitted_entry,
                                                          'just_submitted': just_submitted, 'cur_time': cur_time, 'entry_feed': entry_feed})

def about(request):
    return TemplateResponse(request,'game/about.html',{})

def tutorial(request):
    return TemplateResponse(request,'game/tutorial.html',{})

def handler404(request):
    return render(request,'game/404.html')

def handler500(request):
    return render(request,'game/500.html')
