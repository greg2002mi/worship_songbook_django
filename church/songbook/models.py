import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.utils import timezone
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField

CHORDNOTE=[
    (0, 'Empty'),
    (1, 'C'), 
    (2, 'C#'), 
    (3, 'D'),
    (4, 'D#'),
    (5, 'E'),
    (6, 'F'),
    (7, 'F#'),
    (8, 'G'),
    (9, 'G#'),
    (10, 'A'),
    (11, 'A#'),
    (12, 'B')
    ]

LANG=[
    (0, 'Empty'),
    (1, 'eng'), 
    (2, 'kor'), 
    (3, 'rus'),
    ]

MEDIA=[
    (0, 'other'),
    (1, 'audio'), 
    (2, 'youtube'), 
    (3, 'image'),
    ]

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images/')
    about_me = models.TextField(max_length=140)
    mobile_no = PhoneNumberField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()    

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    language = models.CharField(max_length=5)
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = AutoSlugField(populate_from='title', blank=True, null=True, unique_with=['created_on'])
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title

class Mlinks(models.Model):
    slug = models.CharField(max_length=250)
    filename = models.CharField(max_length=255)
    mtype = models.IntegerField(choices=MEDIA) # 1 - audio, 2 - youtube, 3 - image
    murl = models.CharField(max_length=140)


class Tag(models.Model):
    name = models.CharField(max_length=70)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique_with=['created_on'])

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=140)
    info = models.TextField(max_length=140)
    key = models.IntegerField(choices=CHORDNOTE)
    minor = models.BooleanField(default=False)
    lyrics = models.TextField(blank=True, null=True)
    language = models.IntegerField(choices=LANG)
    timestamp = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='song')
    tags = models.ManyToManyField(Tag, blank=True, related_name='song')
    translated = models.ManyToManyField('Song', blank=True, related_name='translation')
    media = models.ManyToManyField(Mlinks, related_name='song', blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = AutoSlugField(populate_from='title', unique_with=['timestamp'])
    
    def __str__(self):
        return self.title

class Image(models.Model):
    filename = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="image")
    
    class Meta:
        ordering=['-date']
        
    def __str__(self):
        return str(self.date)

class Lists(models.Model):
    title = models.CharField(max_length=100, default='Sunday service')
    created = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    mlink = models.CharField(max_length=140)
    passage = models.TextField() # passage on first page of stage mode
    status = models.IntegerField(default=0)
    assigned = models.ManyToManyField(User, related_name='created')
    slug = AutoSlugField(populate_from='title', unique_with=['created'])

class ListItem(models.Model):
    title = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    desired_key = models.IntegerField(choices=CHORDNOTE)
    listorder = models.IntegerField()
    notes = models.TextField()
    lists = models.ForeignKey(Lists, on_delete=models.CASCADE, related_name='items')
    assigned = models.ManyToManyField(User, related_name='assigned')
    song = models.ManyToManyField(Song, related_name='inlist') 
    slug = AutoSlugField(populate_from='title', unique_with=['created'])

    