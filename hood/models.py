from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
from tinymce.models import HTMLField
from django.dispatch import receiver

class Hood(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Status(models.Model):
    status_content = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-date_posted',)
    
    @classmethod
    def status_by_user(cls, username):
        status = Status.objects.filter(user__username = username)
        return status
    
    @classmethod
    def status_by_hood(cls, hood_name):
        status = Status.objects.filter(hood__name = hood_name)
        return status
    
    def __str__(self):
        return self.user.username

class Business(models.Model):
    business_name = models.CharField(max_length=100)
    business_email = models.EmailField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)
    business_hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.business_name
    
    @classmethod
    def get_business_by_user(cls, username):
        businesses = Business.objects.filter(user__username=username)
        return businesses

class Bio(models.Model):
    nickname = models.CharField(max_length=50, blank=True)
    user_bio = models.TextField(blank=True)
    user_upic = ImageField(blank=True, manual_crop='')
    user_hood = models.ForeignKey(Hood, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @classmethod
    def get_bio_by_user(cls, username):
        profile = Bio.objects.get(user__username = username)
        return profile

    def __str__(self):
        return self.user.username

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Bio.objects.create(user=instance)
        except Exception as error:
            print(error)

class Image(models.Model):
    photo = ImageField(blank=True, manual_crop='')
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    def save_image(self):
        self.save()
    
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk = profile)
        return images

class Profile(models.Model):
    prof_pic = ImageField(blank=True, manual_crop='')
    bio = HTMLField()
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
