from django.contrib import admin
from .models import (
    SubscriptionPlan, UserProfile, Tip, Follower,
    ChatMessage, Subscription, Sport, Team,
    Fixture, Result, LiveScore, SportsOdds, TipsterStats
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
    search_fields = ('user__username', 'sport', 'bet_type')  # Adjust as per your fields


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
    list_display = ('league', 'home_team', 'home_score', 'away_team', 'away_score', 'match_status', 'match_time')
    # You can add more admin configurations as needed



@admin.register(SportsOdds)
class SportsOddsAdmin(admin.ModelAdmin):
    list_display = ('fixture', 'team_home_odds', 'team_away_odds', 'draw_odds')
    

@admin.register(TipsterStats)
class TipsterStatsAdmin(admin.ModelAdmin):
    # Customize the display of TipsterStats in the admin panel if needed
    list_display = ('user', 'total_bets_placed', 'total_wins', 'points_balance', 'last_points_reset')
