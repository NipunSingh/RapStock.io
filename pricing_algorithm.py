from django.core.management.base import BaseCommand, CommandError
from game.models import Artist, ArtistData, GameUser, GameUserData, Investment
import random
import requests


class Command(BaseCommand):

    #method run once an hour by Django to calculate the stock price for each artist
    def handle(self, *args, **options):
        all_artists = Artist.objects.all()
        for artist in all_artists:
            try:
                spotify_data = self.get_spotify_data(artist)
                price = self.compute_artist_price(spotify_data)
                self.update_artist(artist, price, spotify_data)
            except:
                pass
        self.update_investments()
        self.update_users()

    def get_spotify_data(self, artist):
        cleaned_artist_name = artist.name.replace(" ", "%20")
        r = requests.get('https://api.spotify.com/v1/search?q=' + cleaned_artist_name + '&type=artist').json()
        popularity = r['artists']['items'][0]['popularity']
        id = r['artists']['items'][0]['id']
        artist_request = requests.get('https://api.spotify.com/v1/artists/' + id).json()
        followers = artist_request['followers']['total']
        return (popularity, followers)

    def compute_artist_price(self, spotify_data):
        popularity = spotify_data[0]
        followers = spotify_data[1]
        # pricing algo for lower popularity artists
        if (popularity < 57):
            variability = (popularity - 35.0) / 100.0
            noisy_popularity = popularity + random.gauss(0, variability)  # adding noise to spotify popularity
            price = (noisy_popularity - 45) * .56 + 2
            if (price < 2):
                price = 1.50  # price floor
        # pricing algo for higher popularity artists
        if (popularity >= 57):
            variability = (popularity - 30.0) / 100.0
            noisy_popularity = popularity + random.gauss(0, variability)  # adding noise to spotify popularity
            price = (noisy_popularity - 50) * 1.70 + (popularity - 73) * .2
            # extra price for very high popularity artists to create increased differentiation
            if (popularity > 81):
                price += (popularity - 82) * 0.4 * random.gauss(1, 0.01)
            if (popularity > 88):
                price += (popularity - 88) * 0.6 * random.gauss(1, 0.02)
            if (popularity > 92):
                price += (popularity - 92) * .75 * random.gauss(1, 0.03)
        rounded_price = round(price, 2)
        return rounded_price

    def update_artist(self, artist, price, spotify_data):
        cur_artist = artist
        cur_artist.price = price
        cur_artist.save()
        new_data = ArtistData(media=artist, value=price, spotify_popularity=spotify_data[0],
                              spotify_followers=spotify_data[1])
        new_data.save()

    def update_investments(self):
        investment_list = Investment.objects.all().exclude(shares=0)
        for investment in investment_list:
            if(investment.shares > 0):
                investment.value = investment.shares * investment.media.price
                investment.save()

    def update_users(self):
        all_users = GameUser.objects.all()
        for user in all_users:
            net_worth = user.free_points
            if (net_worth < 0):
                net_worth = 0
                user.free_points = 0
                user.save()
            users_investments = Investment.objects.all().filter(user=user).exclude(shares=0)
            invested_points = 0
            for investment in users_investments:
                if (investment.shares > 0):
                    net_worth += investment.shares * investment.media.price
                    invested_points += investment.shares * investment.media.price
            if (net_worth >= 0 and net_worth < 99999.99 and invested_points >= 0 and invested_points < 99999.99):
                user.points = net_worth
                user.invested_points = invested_points
                user.save()
                cur_user_data = GameUserData(user=user, points=net_worth, invested_points=user.invested_points,
                                             free_points=user.free_points)
                cur_user_data.save()
