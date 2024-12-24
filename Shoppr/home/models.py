import html

from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import  ModelForm, TextInput, Textarea
from django.contrib.auth.models import User

# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayir'),
        
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    company = models.CharField(max_length=50)
    adress = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField( blank=True, max_length=15)
    email = models.CharField( blank=True, max_length=50)
    smtpserver = models.CharField(blank=True ,max_length=20)
    smtpemail = models.CharField(blank=True ,max_length=20)
    smtppasword = models.CharField(blank=True ,max_length=20)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True ,upload_to='home')
    facebook = models.CharField(blank=True ,max_length=50)
    instagram = models.CharField(blank=True ,max_length=50)
    twitter = models.CharField(blank=True ,max_length=50)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.icon.url))
    image_tag.short_description = 'Image'


class ContactFormMessage(models.Model):
        STATUS = (
            ('New', 'New'),
            ('Read', 'Read'),
            ('Closed','Closed'),

        )
        name = models.CharField(blank=True, max_length=20)
        email = models.CharField(blank=True, max_length=50)
        subject = models.CharField(blank=True, max_length=50)
        message = models.CharField(blank=True, max_length=255)
        status = models.CharField( max_length=20, choices=STATUS, default='New')
        ip = models.CharField(blank=True, max_length=20)
        note = models.CharField(blank=True, max_length=100)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.name

        def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)

class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject','message']
        widgets = {
             'name'          : TextInput(attrs={'class': 'input', 'placeholder':'Ad və Soyadınız'}),
             'email'         : TextInput(attrs={'class' : 'input', 'placeholder':'Email adresiniz'}),
             'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Mövzu'}),
             'message'       : Textarea(attrs={'class': 'input', 'placeholder':'Bizə yazın','rows' :'10'}),

    }


class Slider(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayir'),

    )
    title = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to='home')
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    promotion1=models.TextField(blank=True)
    promotion2 = models.TextField(blank=True)
    promotion3 = models.TextField(blank=True)
    promotion4 = models.TextField(blank=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    adress = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=40)
    country = models.CharField(blank=True, max_length=60)
    image = models.ImageField(blank=True, upload_to='user')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return  self.user.first_name +' '+self.user.last_name +'['+self.user.username +']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'



class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone', 'adress', 'city', 'country', 'image']







