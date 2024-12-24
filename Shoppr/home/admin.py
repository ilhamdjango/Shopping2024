from django.contrib import admin
from .models import Setting,ContactFormMessage, Slider,UserProfile


# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','status','image_tag']
    list_filter = ['status',]
    readonly_fields = ('image_tag',)


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display=['name', 'email','subject','message','note', 'status']
    list_filter=['status']


class SliderAdmin(admin.ModelAdmin):
        list_display = ['title','image']

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user_name','phone', 'adress','city','image_tag']
    readonly_fields = ('image_tag',)


    
    
admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(UserProfile,UserProfileAdmin)

