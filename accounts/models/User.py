import uuid
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models



'''

https://www.rfc-editor.org/rfc/rfc5321#section-2.3.11
According to this RFC, the local part of the address before the @ is to be 
handled by the mail host at its own terms, 
it mentions nothing about a standard requiring the local part to be lowercase, 
neither to handle addresses in a case insensitive way, 
even if most mail servers will do so nowadays.

This means that a mail server actually can discard mails sent to 
user.name@mail.tld if the account is set up as User.Name@mail.tld. 
This is also reflected in the original normalize_email method of Django's BaseUser class, 
it only forces the domain part to be lowercase for this reason. 
Considering this, we have to store the local part of the address in is original format.
'''

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a valid password')

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user



'''
Through tables for accept and block list
'''


class User(AbstractUser):

    objects = CustomUserManager()
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    username = None
    email = models.EmailField(unique=True)

    subscription = models.ForeignKey(
        to='SubscriptionType',

        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name='Subscription type',
        help_text='Default code = default ',
        related_name='users',  # relate the ForeignKey field with reverse relationships,
        db_constraint=False
    )

    subscription_active = models.BooleanField(default=True, null=True, blank=True)
    subscription_type = models.TextField(default='', blank=True, null=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_renewal_date = models.DateField(null=True, blank=True)
    subscription_notes = models.TextField(default='', blank=True, null=True)

    is_out_of_office = models.BooleanField(default=False)
    out_of_office_until = models.DateTimeField(null=True, blank=True)


    contact_details = models.TextField(default='', blank=True, null=True)
    preferred_name = models.CharField(max_length=200, default='', blank=True, null=True)

    street_name = models.CharField(max_length=200, default='', blank=True, null=True)
    suburb = models.CharField(max_length=100, default='', blank=True, null=True)
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    state = models.CharField(max_length=20, default='', blank=True, null=True)
    postcode = models.CharField(max_length=5, default='', blank=True, null=True)
    phone = models.CharField(max_length=15, default='', blank=True, null=True)

    # privacy settings - the simplest solution to begin with
    allow_public = models.BooleanField(default=False, blank=True, null=True)

    # For the future
    allow_same_domain = models.BooleanField(default=False, blank=True, null=True)
    allow_same_country = models.BooleanField(default=False, blank=True, null=True)
    allow_same_region = models.BooleanField(default=False, blank=True, null=True)
    allow_same_locality = models.BooleanField(default=False, blank=True, null=True)
    allow_same_postcode = models.BooleanField(default=False, blank=True, null=True)



    '''
    From whom am I going to allow contact/invitations
    '''
    acceptable = models.ManyToManyField(
        to='self',
        related_query_name='approved_inviters',
        db_index=True,
        verbose_name='Users allowed to invite',
        help_text='Users who can invite this user to join a group.',
        blank=True,
        through='UserAcceptlist'
    )

    blocklist = models.ManyToManyField(
        to='self',
        related_query_name='blocked_contacts',
        db_index=True,
        verbose_name='Users not allowed to make contact',
        help_text='Users who have been blocked by this user.',
        blank=True,
        through='UserBlocklist',
    )







    # the following fields need to added after core has initial migrated
    # to avoid cyclical dependency, these two fields are commented out for account initial migration




    @property
    def name(self):
        if self.preferred_name:
            return self.preferred_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email

    from django.utils import timezone

    def set_out_of_office_on_save(self):
        now = timezone.now()
        if self.out_of_office_until:
            if now < self.out_of_office_until:
                self.is_out_of_office = True
            else:
                self.is_out_of_office = False
                self.out_of_office_until = None
        else:
            self.is_out_of_office = False

    def save(self, *args, **kwargs):
        self.set_out_of_office_on_save()
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['email']
        verbose_name = "User"
        verbose_name_plural = "Users"
