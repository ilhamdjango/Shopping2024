from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from .models import Categories, Product,Images,Comment



class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5
    # Bu producta elave 5 sekil yuklemek ucundur o 5 sekil producta gorsenir

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title','status','image_tag']
    list_filter = ['status',]
    readonly_fields = ('image_tag',)
    # Bu artiq islemir Alt kategoriye gore Admin2 duzeldib onunla isledik
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'price', 'amount', 'status','image_tag','sale','new','kampaniya','popular']
    list_filter = ['price', 'category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]  # Bu asagiya 5 sekil gostermek ucundur
    #Burdaki readonly fields adminde sekil acmaq ucundur
    
    
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'title','image_tag']
    list_filter = ['product','title', ]
    readonly_fields = ('image_tag',)

#Buradan
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count',)
    list_display_links = ('indented_title',)




    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Categories.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Categories.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs


    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
    # Bura qeder copy paste elemisem bu alt katogoriya duzelmek ucundur

class CommentAdmin(admin.ModelAdmin):
        list_display = [ 'comment','subject', 'product', 'user', 'status','rate']
        list_filter = ['status']


    
admin.site.register(Categories, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)


