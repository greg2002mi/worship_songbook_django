from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    
    path("", views.PostList.as_view(), name="index"),
    path("index", views.PostList.as_view(), name="index"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("contact_us", views.contact_us, name="contact_us"),
    path("profile/", views.profile, name="profile"),
    path("post_detail/<int:post_id>", views.post_detail, name="post_detail"),
    path("songbook", views.songbook, name="songbook"),
    path("explore", views.explore, name="explore"),
    path("make_post", views.make_post, name="make_post"),
    path("confirm_post/<int:post_id>", views.confirm_post, name="confirm_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
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
    #path("<int:song_id>/upload_i", views.upload_i, name="upload_i"),
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
    path("add_to_cart/<int:songid>/<int:c>/<str:keyword>", views.add_to_cart, name="add_to_cart"),
    path("events", views.events, name="events"),
    
    path("change_password", views.change_password, name="change_password"),
    
    
    path("calendar", views.calendar, name="calendar"),
    
    path('jadd_event', views.jadd_event, name='add_event'),
    path('jupdate', views.jupdate, name='update'),
    path('jremove', views.jremove, name='remove'),
    
    path('edit_event/<int:listid>', views.edit_event, name='edit_event'),
    path('delete_event/<int:eventid>/<int:jump>', views.delete_event, name='delete_event'),
    path('unsign_from_listitem/<int:item_id>/<str:username>/<int:state>', views.unsign_from_listitem, name='unsign_from_listitem'),
    path('list_delete_item/<int:item>/<int:listid>', views.list_delete_item, name='list_delete_item'),
    path('jall_events', views.jall_events, name='all_events'),
    path('delete_item/<int:item>', views.delete_item, name='delete_item'),
    path('add2event', views.add2event, name='add2event'),
    path('add2xevent', views.add2xevent, name='add2xevent'),
    
    path("assign2event", views.assign2event, name="assign2event"),
    path("add_event", views.add_event, name="add_event"),
    path("lists/<int:list_id>", views.lists, name="lists"),
    
    path('onstage/<int:eventid>/<int:viewtype>', views.onstage, name='onstage'),
    
    path('cart', views.cart, name='cart'),
    path('empty_cart', views.empty_cart, name='empty_cart'),
    path('unsign_from_cartitem/<int:item_id>/<str:username>/<int:state>', views.unsign_from_cartitem, name='unsign_from_cartitem'),
    path('cart_update_list_order', views.cart_update_list_order, name='cart_update_list_order'),
    path('cart_update_desired_key', views.cart_update_desired_key, name='cart_update_desired_key'),
    path('cart_update_notes', views.cart_update_notes, name='cart_update_notes'),
    path('cart_assign_user', views.cart_assign_user, name='cart_assign_user'),
    ]

