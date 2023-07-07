from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Post, Mlinks, Tag, Song, Lists, ListItem, Image, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class SongAdmin(admin.ModelAdmin):
    list_display = ( 'id','title', 'singer', 'key', 'minor', 'get_publisher', 'status','timestamp')
    list_filter = ("title",)
    search_fields = ['title', 'singer','lyrics']
    
    def get_publisher(self, obj):
        return obj.publisher.username
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ( 'filename','image', 'song')
    list_filter = ("song",)
    search_fields = ['filename', 'song']

class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default UserAdmin
admin.site.unregister(User)
# Register the custom UserAdmin
admin.site.register(User, UserAdmin)

admin.site.register(Post, PostAdmin)
admin.site.register(Mlinks)
admin.site.register(Tag)
admin.site.register(Song, SongAdmin)
admin.site.register(Lists)
admin.site.register(ListItem)
admin.site.register(Image)