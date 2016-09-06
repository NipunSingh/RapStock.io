from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class GameUser(models.Model):
    user = models.OneToOneField(User)
    points = models.DecimalField(max_digits=7, decimal_places=2)
    invested_points = models.DecimalField(max_digits=7, decimal_places=2)
    free_points = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return u'%s' % self.user.username


class GameUserData(models.Model):
    user = models.ForeignKey(GameUser) #Who owns the trade
    date = models.DateTimeField('date created', auto_now_add=True)
    points = models.DecimalField(max_digits=7, decimal_places=2)
    invested_points = models.DecimalField(max_digits=7, decimal_places=2)
    free_points = models.DecimalField(max_digits=7, decimal_places=2)
    rank = models.IntegerField(null=True,blank=True)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.TextField(max_length=1000,null=True,blank=True)
    long_description = models.TextField(max_length=2000,null=True,blank=True)
    icon_URL = models.TextField(max_length=500,null=True,blank=True)
    cover_URL = models.TextField(max_length=500,null=True,blank=True)
    pic3_URL = models.TextField(max_length=500,null=True,blank=True)
    soundcloud_URL = models.TextField(max_length=1000,null=True,blank=True)
    metric = models.TextField(max_length=500,null=True,blank=True)
    metric2 = models.TextField(max_length=500,null=True,blank=True)
    youtube_URL = models.TextField(max_length=500,null=True,blank=True)
    twitter_URL = models.TextField(max_length=500,null=True,blank=True)
    is_featured = models.BooleanField(null=False,blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)
    yesterday_price = models.DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)
    week_price = models.DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)
    soundcloud_id = models.TextField(max_length=200,null=True,blank=True)
    NSB_id = models.TextField(max_length=200,null=True,blank=True)

    def __unicode__(self):
        return u'%s' % self.name


class Investment(models.Model):
    user = models.ForeignKey(GameUser)
    media = models.ForeignKey(Artist)
    buy_price = models.DecimalField(max_digits=6, decimal_places=2,default=5)
    sell_price = models.DecimalField(max_digits=6, decimal_places=2, null=True,blank=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    shares = models.DecimalField(max_digits=7, decimal_places=2, null=True,blank=True) #Shares bought
    buy_date = models.DateTimeField('date created', auto_now_add=True)
    sell_date = models.DateTimeField(null=True,blank=True)

    def __unicode__(self):
        return u'%s traded %d in  %s' % (self.user, self.value, self.media)


class ArtistData(models.Model):
    media = models.ForeignKey(Artist)
    date = models.DateTimeField('date created', auto_now_add=True)
    value = models.DecimalField(max_digits=6, decimal_places=2, null=True,blank=True)
    spotify_followers = models.IntegerField(null=True,blank=True)
    spotify_popularity = models.IntegerField(null=True,blank=True)
    youtube_views =  models.IntegerField(null=True,blank=True)
    youtube_downvotes =  models.IntegerField(null=True,blank=True)
    vevo_views = models.IntegerField(null=True,blank=True)
    wikipedia_view = models.IntegerField(null=True,blank=True)
    twitter_mentions = models.IntegerField(null=True,blank=True)
    twitter_retweets = models.IntegerField(null=True,blank=True)
    sentiment = models.IntegerField(null=True,blank=True)
    billboard_ranking = models.IntegerField(null=True,blank=True)
    billboard_ranking2 = models.IntegerField(null=True,blank=True)
    type = models.TextField(max_length=500,null=True,blank=True)
    category = models.TextField(max_length=500,null=True,blank=True)

    def __unicode__(self):
        return u'%s at %d' % (self.media, self.value)


class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000,null=True,blank=True)
    in_game_price = models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
    real_price = models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
    amazon_image = models.TextField(max_length=2000,null=True,blank=True)
    amazon_graphic = models.TextField(max_length=2000,null=True,blank=True)
    name_link = models.TextField(max_length=1000,null=True,blank=True)
    alt_image_url = models.TextField(max_length=1000,null=True,blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class GrammyEntry(models.Model):
    user = models.ForeignKey(GameUser)
    date = models.DateTimeField('date created', auto_now_add=True)
    choice1 = models.TextField(max_length=150,null=True,blank=True)
    choice2 = models.TextField(max_length=150,null=True,blank=True)
    choice3 = models.TextField(max_length=150,null=True,blank=True)
    choice4 = models.TextField(max_length=150,null=True,blank=True)
    choice5 = models.TextField(max_length=150,null=True,blank=True)
    number_correct = models.IntegerField(null=True,blank=True)
