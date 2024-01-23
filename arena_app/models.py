# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone


# USERS

class SubscriptionPlan(models.Model):
    """
    Represents a subscription plan in the application.

    Attributes:
        name (str): The name of the subscription plan.
        price_monthly (Decimal): The monthly price of the subscription plan.
        price_yearly (Decimal): The yearly price of the subscription plan.
    """

    name = models.CharField(max_length=50, unique=True)
    price_monthly = models.DecimalField(max_digits=6, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class UserProfileManager(BaseUserManager):
    """
    Custom manager for the User Profile model.
    """

    def create_user(self, email, username,
                    name, password=None, **extra_fields):
        """
        Creates and saves a new user with the given details.

        Args:
            email (str): The email address of the user.
            username (str): The username of the user.
            name (str): The name of the user.
            password (str, optional): The password of the user. Defaults to None.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: The newly created user.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name,
                         password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given details.

        Args:
            email (str): The email address of the superuser.
            username (str): The username of the superuser.
            name (str): The name of the superuser.
            password (str, optional): The password of the superuser. Defaults to None.
            **extra_fields: Additional fields to be saved in the superuser model.

        Returns:
            User: The newly created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, name,
                                password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user profile in the system.

    Attributes:
        name (str): The name of the user.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        is_staff (bool): Indicates if the user is a staff member.
        is_active (bool): Indicates if the user is active.

        subscription_status (bool): Indicates the subscription status of the user.
        subscription_type (str): The type of subscription the user has.
        subscription_plan (SubscriptionPlan): The subscription plan associated with the user.

        points_balance (int): The current balance of points for the user.
        last_points_reset (date): The date when the points were last reset.

        total_bets_placed (int): The total number of bets placed by the user.
        total_wins (int): The total number of wins by the user.

    Properties:
        win_rate (float): The win rate of the user, calculated as the percentage of wins out of total bets placed.
        average_odds (float): The average odds of the user's tips.

    Methods:
        reset_points(): Resets the points balance of the user to the default value.

    Relationships:
        groups (ManyToManyField): The groups the user belongs to.
        user_permissions (ManyToManyField): The specific permissions granted to the user.

    Managers:
        objects (UserProfileManager): The manager for the UserProfile model.

    """

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Add additional fields for the user profile
    subscription_status = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=10, blank=True, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan,
                                          on_delete=models.SET_NULL, null=True,
                                          blank=True)

    # Additional fields for the points system
    points_balance = models.IntegerField(default=1000)
    last_points_reset = models.DateField(auto_now_add=False,
                                         default=timezone.now)

    # New fields for tipster stats
    total_bets_placed = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)

    # Properties to calculate win rate and average odds
    @property
    def win_rate(self):
        if self.total_bets_placed > 0:
            return (self.total_wins / self.total_bets_placed) * 100
        return 0

    @property
    def average_odds(self):
        return self.tips.aggregate(Avg('odds'))['odds__avg'] or 0
    
    # Update the points balance (can be called monthly or as needed)
    def reset_points(self):
        self.points_balance = 1000
        self.last_points_reset = timezone.now().date()
        self.save()

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_profiles',
        related_query_name='user_profile',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_profiles',
        related_query_name='user_profile',
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username

# SPORTS


class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    # Add any additional fields for sports (e.g., image, description, etc.)


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    # Add any additional fields for teams (e.g., logo, description, etc.)


class Fixture(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  related_name='home_fixtures')
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  related_name='away_fixtures')
    date_time = models.DateTimeField()

    def __str__(self):
        return self.sport
    # Add any additional fields for fixtures (e.g., venue, status, etc.)


class Tip(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tips')
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Sport
    bet_type = models.CharField(max_length=100, null=True, blank=True)  # e.g., Match Odds, Correct Score
    odds = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    points_bet = models.IntegerField(default=0) # Points wagered
    is_win = models.BooleanField(null=True, blank=True)  # True if win, False if loss, null if undecided
    created_at = models.DateTimeField(auto_now_add=True)
    additional_info = models.JSONField(blank=True, null=True)  # For storing dynamic bet details

    def __str__(self):
        user_username = self.user_username if self.user else 'Unknown User'
        sport_name = self.sport.name if self.sport else 'Unknown Sport'
        return f"{user_username} - {sport_name}"

# New model for TipsterStats
class TipsterStats(models.Model):
    """
    Represents the statistics and points balance of a tipster user.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='tipster_stats')
    total_bets_placed = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    points_balance = models.IntegerField(default=1000)
    last_points_reset = models.DateField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.user.username if self.user else 'Unknown User'

    @property
    def win_rate(self):
        """
        Calculates the win rate of the tipster as a percentage.

        Returns:
            float: The win rate of the tipster.
        """
        if self.total_bets_placed > 0:
            return (self.total_wins / self.total_bets_placed) * 100
        return 0

    @property
    def average_odds(self):
        """
        Calculates the average odds of the tipster's bets.

        Returns:
            float: The average odds of the tipster's bets.
        """
        return self.user.tip_set.aggregate(Avg('odds'))['odds__avg'] or 0

    def reset_points(self):
        """
        Resets the points balance of the tipster to the default value (1000).
        Updates the last points reset date to the current date.
        """
        self.points_balance = 1000
        self.last_points_reset = timezone.now().date()
        self.save()

    def calculate_points_won(self, bet_amount_in_points, odds):
        """
        Calculates the points won by the tipster when a bet is successful.

        Args:
            bet_amount_in_points (int): The amount of points bet on the bet.
            odds (float): The odds of the bet.

        Returns:
            int: The points won by the tipster.
        """
        points_won = int(bet_amount_in_points * (odds - 1))
        self.points_balance += points_won
        self.save()
        return points_won


class Follower(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')


class ChatMessage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()  # Set when the subscription is activated
    status = models.BooleanField(default=True)  # True for active, False for inactive
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES)


class Result(models.Model):
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE)
    team_home_score = models.PositiveIntegerField()
    team_away_score = models.PositiveIntegerField()

    def __str__(self):
        return self.fixture
    # Add any additional fields for results


class LiveScore(models.Model):
    league = models.CharField(max_length=255, default='Unknown League')
    home_team = models.CharField(max_length=255, default='Unknown Team')
    away_team = models.CharField(max_length=255, default='Unknown Team')
    home_score = models.IntegerField(default=0)  
    away_score = models.IntegerField(default=0) 
    match_status = models.CharField(max_length=50,default='Unknown')
    match_time = models.CharField(max_length=50,default='Unknown')
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'arena_app_live_scores'
        unique_together = ('league', 'home_team', 'away_team')

    def __str__(self):
        return f"{self.league}: {self.home_team} vs {self.away_team}"


class SportsOdds(models.Model):
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE)
    team_home_odds = models.FloatField()
    team_away_odds = models.FloatField()
    draw_odds = models.FloatField()

    def __str__(self):
        return self.fixture
    # Add any additional fields for odds


# BLOGS
class BlogPost(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']