from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.forms import  ModelForm, TextInput, Textarea
from django.contrib.auth.models import User


class Categories(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayir'),
        
    )
    title= models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True ,upload_to='category')
    status = models.CharField(max_length=100, choices=STATUS)
    slug = slug = models.SlugField(null=False, db_index=True, unique=True, blank=True, editable=False)
    parent = TreeForeignKey('self', blank= True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


    # Burdan
    class MPTTMeta:
        order_insertion_by = ['title']
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '  >>  '.join(full_path[::-1])
    #Bura qədər kod kateqoriyani alt kateqoriyaya bölmək üçündür
    # Importu --from mptt.models import MPTTModel, TreeForeignKey
    # pip install django-mptt  bunu da install etmek lazimdir




    # Burdan
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Bura qeder Save elemek ucundur


       # Burdan
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
    #Bura Admin sekili adminde acmaq ucundur
    
class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayir'),
        
    )
    SALE = (
    ('True' , 'Evet'),
    ('False', 'Hayir'),
    )
    NEW = (
        ('True', 'Evet'),
        ('False','Hayir'),

    )

    KAMPANİYA =(
        ('True', 'Evet'),
        ('False', 'Hayir'),


    )
    POPULAR=(
        ('True', 'Evet'),
        ('False', 'Hayir'),
    )

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True ,upload_to='product')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()   #from ckeditor_uploader.fields import RichTextUploadingField
    status = models.CharField(max_length=10, choices=STATUS,)
    slug = models.SlugField(null=False, db_index=True, unique=True, blank=True, editable=False)
    parent=models.ForeignKey('self', blank= True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    sale = models.CharField(max_length=10, choices=SALE,)
    new = models.CharField(max_length=10, choices=NEW, )
    kampaniya = models.CharField(max_length=10, choices=KAMPANİYA, )
    popular= models.CharField(max_length=10, choices=POPULAR, )

    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='product')    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Evet'),
        ('False','Hayir'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50,blank=True)
    comment=models.TextField(max_length=200,blank=True)
    rate = models.IntegerField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject' , 'comment' ,'rate' ]


