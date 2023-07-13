from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="index"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("songbook", views.songbook, name="songbook"),
    path("song/add/", views.add_song, name="add_song"),
    path("<int:song_id>/<int:key>/view_song", views.view_song, name="view_song"),
    path("<int:song_id>/edit_song", views.edit_song, name="edit_song"),
    path("<int:song_id>/delete_song", views.delete_song, name="delete_song"),
    path("<int:song_id>/upload_audio", views.upload_audio, name="upload_audio"),
    path("<int:song_id>/upload_video", views.upload_video, name="upload_video"),
    path("<int:image_id>/<int:song_id>/delete_image", views.delete_image, name="delete_image"),
    path("<int:audio_id>/<int:song_id>/delete_audio", views.delete_audio, name="delete_audio"),
    path("<int:mlink_id>/<int:song_id>/delete_video", views.delete_video, name="delete_video"),
    path("<int:song_id>/manage_media", views.manage_media, name="manage_media"),
    path("<int:song_id>/upload_i", views.upload_i, name="upload_i"),
    path("<int:song_id>/add_transl", views.add_transl, name="add_transl"),
    path("remove_transl/<int:selsong_id>/<int:cursong_id>", views.remove_transl, name="remove_transl"),
    path("<int:song_id>/tagging", views.tagging, name="tagging"),
    path("tag_list", views.tag_list, name="tag_list"),
    path("<int:tag_id>/delete_tag", views.delete_tag, name="delete_tag"),
    path("<int:tag_id>/tag_songlist", views.tag_songlist, name="tag_songlist"),
    path("<int:song_id>/untagall", views.untagall, name="untagall"),
    path("<int:tag_id>/<int:song_id>/untag", views.untag, name="untag"),
    path("publish/<int:song_id>/", views.publish, name="publish"),
    path("<int:mtype>/<int:song_id>/upload_images", views.file_upload, name="upload_images"),
    path("<int:user_id>/avatar_upload", views.avatar_upload, name="avatar_upload"),
    path("<int:song_id>/add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("events", views.events, name="events"),
    path("calendar", views.calendar, name="calendar"),
    path("add_event", views.add_event, name="add_event"),
    path("lists/<int:list_id>", views.lists, name="lists"),
    ]

# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()