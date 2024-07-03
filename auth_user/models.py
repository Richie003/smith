from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, tel, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, tel, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, tel, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        OWNER = "Owner", "owner"
        CUSTOMER = "Customer", "customer"

    base_role = Role.CUSTOMER
    objects = UserManager()
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True, null=True
    )
    username = models.CharField(
        default="",
        verbose_name="username",
        unique=True,
        null=True,
        blank=False,
        max_length=30,
    )
    tel = models.CharField(default="", null=True, blank=True, max_length=11)
    category = models.CharField(default="CUSTOMER", max_length=50, choices=Role.choices)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "tel"]  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        # concatenate = '%s %s' % (self.first_name, self.last_name)
        return str(self.username)

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active


class CustomerBio(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    display_photo = models.ImageField(
        upload_to="display_photo/", default="profile.png", blank=True
    )
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)


class WeekDay(models.Model):
    day = models.CharField(max_length=10, default="", blank=True, null=False)

    def __str__(self):
        return str(self.day)


class RestaurantBio(models.Model):
    name = models.CharField(max_length=100)
    owned_by = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    open_by = models.TimeField(default="07:59:00")
    close_by = models.TimeField(default="22:59:00")
    week_days = models.ManyToManyField(WeekDay)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def count_days_available(self):
        return self.week_days.count

    @property
    def week_days_abbrev(self):
        abbrevs = {
            "Sunday": "Sun",
            "Monday": "Mon",
            "Tuesday": "Tue",
            "Wednesday": "Wed",
            "Thursday": "Thur",
            "Friday": "Fri",
            "Saturday": "Sat",
        }

        week_days = list(self.week_days.all())
        if not week_days:
            return []

        first_day = week_days[0].day
        last_day = week_days[-1].day

        print(f"firstDay: {first_day}\nlastDay: {last_day}")

        first_day_abbrev = abbrevs.get(first_day, "")
        last_day_abbrev = abbrevs.get(last_day, "")

        return "%s - %s" % (first_day_abbrev, last_day_abbrev)
        # assert (day[0] for i, day in enumerate(abbrevs)) == first_day
