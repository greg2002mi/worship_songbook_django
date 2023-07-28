from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import os

# Register your models here.
from .models import Post, Mlinks, Tag, Song, Lists, ListItem, Image, Audio, Profile, BgImg

class PostAdmin(ImportExportModelAdmin):
    list_display = ('title', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    # raw_id_fields = ('user',)
    # date_hierarchy = 'created_on'
    # ordering = ('status', 'created_on')

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ( 'filename','date', 'song', 'audio_file_player')
    actions = ['custom_delete_selected']
    
    def custom_delete_selected(self, request, queryset):
        #custom delete code
        n = queryset.count()
        for i in queryset:
            if i.audio_file:
                if os.path.exists(i.audio_file.path):
                    os.remove(i.audio_file.path)
            i.delete()
        self.message_user(request, ("Successfully deleted %d audio files.") % n)
    
    custom_delete_selected.short_description = "Delete selected items"

    def get_actions(self, request):
        actions = super(AudioFileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class SongAdmin(ImportExportModelAdmin):
    list_display = ( 'id','title', 'singer', 'key', 'minor', 'get_publisher', 'status','timestamp')
    list_filter = ("title",)
    search_fields = ['title', 'singer','lyrics']
    
    def get_publisher(self, obj):
        return obj.publisher.username
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ( 'filename','image', 'song')
    list_filter = ("song",)
    search_fields = ['filename', 'song']
    
class BgIgmAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'filename','image')
    list_filter = ("title",)
    search_fields = ['title', 'filename', 'song']
    
class TagAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'created_on')
    list_filter = ("name",)
    search_fields = ['name',]
    
class ListItemsAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'created', 'desired_key', 'listorder', 'notes')
    list_filter = ("title",)
    search_fields = ['title',]


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
admin.site.register(Audio, AudioFileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Mlinks)
admin.site.register(Tag, TagAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Lists)
admin.site.register(ListItem, ListItemsAdmin)
admin.site.register(Image)
admin.site.register(BgImg, BgIgmAdmin)