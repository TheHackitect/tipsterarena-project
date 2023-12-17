from django.contrib import admin
from .models import (
    SubscriptionPlan, UserProfile, Tip, Follower,
    ChatMessage, Subscription, Sport, Team,
    Fixture, Result, LiveScore, SportsOdds
)

# USERS


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_monthly', 'price_yearly')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email', 'subscription_status', 'subscription_type', 'subscription_plan')
    search_fields = ('user__username', 'user__email', 'name')


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport', 'bet_type', 'odds', 'points_bet', 'is_win', 'created_at')
    search_fields = ('user__username', 'sport', 'bet_type') # Adjust as per your fields


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status', 'subscription_type')

# SPORTS


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport')


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('sport', 'team_home', 'team_away', 'date_time')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('fixture', 'team_home_score', 'team_away_score')


@admin.register(LiveScore)
class LiveScoreAdmin(admin.ModelAdmin):
    list_display = ('fixture', 'team_home_score', 'team_away_score', 'status')


@admin.register(SportsOdds)
class SportsOddsAdmin(admin.ModelAdmin):
    list_display = ('fixture', 'team_home_odds', 'team_away_odds', 'draw_odds')
