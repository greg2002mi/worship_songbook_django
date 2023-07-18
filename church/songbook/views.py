from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.paginator import (EmptyPage, PageNotAnInteger,
Paginator)
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post, Mlinks, Tag, Song, Lists, ListItem, Image, LANG, CHORDNOTE, Audio
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext as _
from .forms import AddSongForm, Transpose, AddTagForm, TagsForm, SongsForm, EmptyForm, EditSongForm, Assign2Event, NewUForm, UpdateUForm, UpdateProfileForm, UploadAvatarForm, AddSongTagForm, AddMediaForm, AddEventForm
from .core import Chordpro_html
from django import forms
import os, uuid, json
from django.contrib import messages
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from datetime import datetime
from django.utils import timezone

PAGE_SIZE = getattr(settings, "PAGE_SIZE", 50)

# splits text into two columns 
def split_text(text, viewtype, ori_key_int, transpose):
    lyrics = ""
    lines = text.split('\n')
    first_part = []
    second_part = []
    count = 0
    half_total = len(lines)/2
    
    
    for line in lines:
        if count < half_total:
            first_part.append(line)
        else:
            if line.strip() == '':
                second_part.append(line)
                second_part.extend(lines[count+1:])
                break
            else:
                first_part.append(line)
        count += 1
    
    first = '\n'.join(first_part) 
    second = '\n'.join(second_part)
    
    if viewtype == 1:
        html1 = Chordpro_html(first, 1, ori_key_int, transpose)
        html2 = Chordpro_html(second, 1, ori_key_int, transpose)
    elif viewtype ==2:
        html1 = Chordpro_html(first, False, 0, 0)
        html2 = Chordpro_html(second, False, 0, 0)
    
    lyrics = '<div class="row"><div class="col-auto">&nbsp;</div><div class="col-5">{}</div><div class="col-5"><br><br><br><br><br>{}</div></div>'.format(html1, html2)
    
    return lyrics

def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, _("You are now logged in as {}.").format(username))
                return redirect("index")
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Invalid username or password."))
    form = AuthenticationForm()
    return render(request, "login.html", context={"form":form})

def logout_page(request):
    logout(request)
    messages.info(request, _("You have successfully logged out."))
    return redirect('index')

def register_page(request):
    if request.method == "POST":
        form = NewUForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Registration successful."))
            return redirect("login")
        messages.error(request, _("Unsuccessful registration. Invalid information."))
    form = NewUForm()
    return render (request, "register.html", context={"form":form})
    
    

@login_required
def profile(request):
    avatar_form = UploadAvatarForm()
    if request.method == 'POST':
        
        user_form = UpdateUForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
    else:
        user_form = UpdateUForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        
    context = {
        'title': _('Songbook'),
        'user_form': user_form,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
    }
    
    return render(request, 'user.html', context)

# function to upload avatar, and delete previous if exists.
def avatar_upload(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        my_file = request.FILES.get('avatar')
        if my_file:
            if user.profile.avatar:
                old_avatar_path = user.profile.avatar.path
                if os.path.isfile(old_avatar_path):
                    os.remove(old_avatar_path)
        newname = '{}{}'.format(uuid.uuid4().hex, os.path.splitext(my_file.name)[1])
        my_file.name = newname # change name of image
        profile = user.profile
        profile.avatar=my_file
        profile.save()
        return redirect('profile')
    messages.error(request, _("Error, failed to POST."))
    return redirect('profile')

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

   
def songbook(request):
    
    songs = Song.objects.filter(status=1).order_by('title')
    songs_all = Song.objects.order_by('title')
    form = AddSongForm()
    tags = Tag.objects.all()
    # page = request.GET.get('page', 1)
    # songs_list = Song.objects.order_by('title')
    paginator = Paginator(songs, PAGE_SIZE)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.get_page(page_number)
        
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    # songs = paginator.get_page(page)
    # next_url = reverse('songbook') + '?page=' + str(songs.next_page_number()) if songs.has_next() else None
    # prev_url = reverse('songbook') + '?page=' + str(songs.previous_page_number()) if songs.has_previous() else None
    
    context = {
        'title': _('Songbook'),
        'songs': songs,
        'songs_all': songs_all,
        # 'next_url': next_url,
        # 'prev_url': prev_url,
        'keyset': CHORDNOTE,
        'lang': LANG,
        'form': form,
        'tags': tags,
        'page_obj': page_obj,
        'c': 2, # here c means return to 2 - return to songbook. 
        'keyword': 'None' # change later
    }
    return render(request, 'songbook.html', context)
 
def add_song(request):
    if request.method == 'POST':
        form = AddSongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.publisher = request.user
            song.save()
            messages.success(request, _("Song successfully created as a draft."))
            return redirect('view_song', song_id=song.pk, key=song.key)  # Redirect to the songbook page after successful submission
    else:
        form = AddSongForm()
    
    return render(request, 'add_song.html', {'form': form})

def publish(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    song.status = 1
    song.save()
    messages.success(request, _("Song has successfully been published."))
    return redirect('songbook')

def view_song(request, song_id, key):
    song = get_object_or_404(Song, pk=song_id)
    tags = Tag.objects.all()
    tag_states = {tag.id: tag in song.tags.all() for tag in Tag.objects.all()}
    images = song.image.all()
    media = song.media.all()
    tagged_list = ()
    # if song.tags:
    #     tagged_list = ([tagged.name for tagged in song.tags])
    # ori_key = ''
    ori_key_int = song.key
    lyrics = song.lyrics
    # upload files
    media_root = settings.MEDIA_ROOT
    # directory = os.path.join(media_root, 'photos')
    files = os.listdir(media_root)
    audio = song.audio.all()
    form = Transpose()
    transl_form = SongsForm()
    remove_transl_form = EmptyForm()
    untagall_form = EmptyForm()
    #to get a list of songs with condition, other language, and not already linked ones
    # other_songs = Song.objects.filter(Song.language!=song.language).all()
    # if song.translated is not None:
    #     linked = song.translated.all()
    #     for l in linked:
    #         other_songs.remove(l)
    # tr_list = [(s.id, s.title) for s in other_songs]
    # transl_form.tr_song_id.choices = tr_list
    # list of translated songs
    t1_songlist = song.translated.order_by('title').all()
    t2_songlist = song.translation.order_by('title').all()
    t_songlist = list(t1_songlist)
    for song_obj in t2_songlist:
        if song_obj not in t_songlist:
            t_songlist.append(song_obj)
    # delete_form = EmptyForm()
    
    tags_form = TagsForm(choices=[(tag.id, tag.name) for tag in Tag.objects.all()])
    # populate choices for tags_form from db
    # choices = [(t.id, t.name) for t in tags]
    # tags_form.name.choices = choices
    # print(choices)
    if key is None:
        transpose = ori_key_int
    else: 
        transpose = int(key)
    # to send original key as string
    key_dict = {'key': transpose}
    ori_key = CHORDNOTE[ori_key_int][1]
    if transpose != ori_key_int:
        ori_key = ori_key + _(" | transposed to ") + CHORDNOTE[transpose][1]
       
    html = Chordpro_html(song.lyrics, True, song.key, transpose)
    only_lyrics = Chordpro_html(lyrics, False, 0, 0)

    if song.lyrics is None:
        messages.success(request, _('Current song does not have lyrics'))
        return redirect('songbook')
    else:
        
        if request.method == 'POST':
            tags_form = TagsForm(request.POST)
            form = Transpose(request.POST)
            if form.is_valid():
                # Handle the submit of transpose chord action
                key = form.cleaned_data['key']
                return redirect('view_song', song_id=song.id, key=key)
            # if tags_form.is_valid():
            #     selected_tags = tags_form.cleaned_data['name']
            #     song.tags.clear()  # Clear existing tags
            #     for tag_id in selected_tags:
            #         tag = Tag.objects.get(id=tag_id)
            #         song.tags.add(tag)
            #     song.save()
            #     # Flash message and redirect
            #     return redirect('view_song', song_id=song.id, key=song.key)
        elif request.method == 'GET':
            
            initial_data = {'name': [tag.id for tag in song.tags.all()]}
            tags_form = TagsForm(initial=initial_data)    
            
        context = {
            'title': _('View Song'),
            'song': song,
            'keyset': CHORDNOTE,
            'lang': LANG,
            'tags': tags,
            'html': html, 
            'transl_form': transl_form, 
            'remove_transl_form': remove_transl_form,  
            'tagged_list': tagged_list, 
            'tag_states': tag_states, 
            'tags_form': tags_form, 
            'only_lyrics': only_lyrics, 
            'form': Transpose(initial=key_dict), 
            'ori_key': ori_key, 
            't_songlist': t_songlist,  
            'untagall_form': untagall_form, 
            'media': media,
            'images': images,
            'audio': audio,
            'files': files,
            
        }
        return render(request, 'view_song.html', context)


def delete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    song.delete()
    # delete song from database
    messages.success(request, _('Song has been permanently deleted.'))
    return redirect('songbook')

@login_required
def edit_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        # to edit add instance of that song, otherwise a new entry will be saved instead
        form = EditSongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, _('Song has been updated successfully.'))
            return redirect('view_song', song_id=song_id, key=song.key)
    else:
        context = {
            'form': EditSongForm(instance=song),
            'song_id': song_id, 
            'song': song,
            }
        return render(request, 'edit_song.html', context)

def upload_audio(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        media = song.audio.all()
        num = len(media) + 1
        newname = "{}.{}_{}.mp3".format(song.id, song.title, str(num))
        original_filename = my_file.name
        my_file.name = newname # change name of image
        audio = Audio.objects.create(audio_file=my_file, title=original_filename, song=song, filename=newname)
        audio.save()
        song.audio.add(audio)
        return redirect('manage_media', song_id=song.id)
    return '', 204

def upload_video(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        form = AddMediaForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.save()
            song.media.add(video)
            messages.success(request, _('Video link has been successfully added.'))
            return redirect('manage_media', song_id=song.id)

def file_upload(request, song_id, mtype):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        media = song.image.all()
        num = len(media) + 1
        newname = "{}.image_{}.jpg".format(song.id, str(num))
        original_filename = my_file.name
        my_file.name = newname # change name of image
        Image.objects.create(image=my_file, title=original_filename, song=song, filename=newname)
        context = {
            'song_id': song_id, 
            'song': song,
            'key': song.key,
            }
        return HttpResponse('view_song', context)
    return JsonResponse({'post':'false'})

def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext) # do instance.username 
                                                    # if you want to save as username
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('images/', filename)

def delete_file(request, song_id, mlink_id):
    pass

def manage_media(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if song.image:
        images = song.image.all()
    else:
        images = []
    if song.audio:
        music = song.audio.all()
    else:
        music = []
    if song.media:
        media = song.media.all()
    else:
        media = []
    form = AddMediaForm()
    context = {
        'song': song, 
        'form': form,
        'images': images,
        'key': song.key,
        'music': music,
        'media': media,
        }
    return render(request, 'manage_media.html', context)

def delete_image(request, song_id, image_id):
    song = get_object_or_404(Song, pk=song_id)
    image = get_object_or_404(Image, pk=image_id)
    if request.method == 'POST':
        # song.image.remove(image)
        image.delete()
        messages.success(request, _('Image has been successfully deleted.'))
        return redirect('manage_media', song_id=song.id)

def delete_audio(request, song_id, audio_id):
    song = get_object_or_404(Song, pk=song_id)
    audio = get_object_or_404(Audio, pk=audio_id)
    if request.method == 'POST':
        # song.audio.remove(audio)
        audio.delete()
        messages.success(request, _('Audio file has been successfully deleted.'))
        return redirect('manage_media', song_id=song.id)
    
def delete_video(request, song_id, mlink_id):
    song = get_object_or_404(Song, pk=song_id)
    video = get_object_or_404(Mlinks, pk=mlink_id)
    if request.method == 'POST':
        song.media.remove(video)
        video.delete()
        messages.success(request, _('Audio file has been successfully deleted.'))
        return redirect('manage_media', song_id=song.id)

def upload_i(request, filename):
    pass

def add_transl(request, song_id):
    current_song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        transl_form = SongsForm(request.POST)
        if transl_form.is_valid():
            oth_song_id = transl_form.cleaned_data['title']
            other_song = get_object_or_404(Song, pk=oth_song_id)
            current_song.translated.add(other_song)
            messages.success(request, _('Translation has been successfully linked.'))
            return redirect('view_song', song_id=current_song.id, key=current_song.key)

def remove_transl(request, selsong_id, cursong_id):
    current_song = get_object_or_404(Song, pk=cursong_id)
    selected_song = get_object_or_404(Song, pk=selsong_id)
    if request.method == 'POST':
        if selected_song in current_song.translated.all():
            current_song.translated.remove(selected_song)
        elif current_song in selected_song.translated.all():
            selected_song.translated.remove(current_song)
            messages.success(request, _('Translation has been successfully unlinked.'))
            return redirect('view_song', song_id=current_song.id, key=current_song.key)
        else:
            messages.error(request, _('Error occured. Please reload page and try again.'))
            return redirect('view_song', song_id=current_song.id, key=current_song.key)

def tag_list(request):
    tags = Tag.objects.all()
    form = AddTagForm()
    deletetag_form = EmptyForm()
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tag is saved successfully.'))
            return redirect('tag_list')
    context = {
        'title': _('Tag list'), 
        'tags': tags, 
        'form': form, 
        'deletetag_form': deletetag_form,
        }
    return render(request, 'tag_list.html', context)

def tag_songlist(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    songs = tag.song.order_by('title')
    paginator = Paginator(songs, PAGE_SIZE)
    page_number = request.GET.get("page")
    addform = AddSongTagForm(tag=tag)
    
    try:
        page_obj = paginator.get_page(page_number)
        
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    # make searchable drop down select
    # if request.method == 'POST':
    #     addform = AddSongTagForm(request.POST)
    #     if addform.is_valid():
    #         song = addform.cleaned_data.get('id')
    #         print(song)
    context = {
        'title': _('Songbook'),
        'songs': songs,
        'keyset': CHORDNOTE,
        'lang': LANG,
        'addform': addform,
        'tag': tag,
        'page_obj': page_obj,
    }
    
        
    return render(request, 'tag_songlist.html', context)
    
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, _('Tag is successfully deleted.'))
        return redirect('tag_list')
    else:
        messages.error(request, _('Error, failed to delete tag.'))
        return redirect('tag_list')


    
def tagging(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    # tag_states = {tag.id: tag in song.tags.all() for tag in Tag.objects.all()}
    
    if request.method == "POST":
        tags_form = TagsForm(request.POST)
        if tags_form.is_valid():
            tagged = tags_form.cleaned_data['name']
            tagged_list = song.tags.all()
            if not tagged_list:
                for dt in tagged_list:
                    song.tags.remove(dt)
            
            #first check if unchecked
            else:
                for tg in tagged_list:
                    if tg.id not in tagged:
                        song.tags.remove(tg)
            
            # add new tags
            for t in tagged:
                song.tags.add(t)
            return redirect('view_song', song_id=song.id, key=song.key) 
        else:
            messages.error(request, _('Error, failed to validate.'))
            return redirect('view_song', song_id=song.id, key=song.key) 
    else:
        messages.error(request, _('Error, failed to add tag to this song.'))
        return redirect('view_song', song_id=song.id, key=song.key)    
    
def untag(request, tag_id, song_id):
    song = get_object_or_404(Song, pk=song_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    song.tags.remove(tag)   
    messages.success(request, _('{} tag is no longer related to this song.'.format(tag.name)))
    return redirect('tag_songlist', tag_id=tag_id)
                    
                    
def untagall(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    for t in song.tags.all():
        song.tags.remove(t)
    song.save()
    messages.success(request, _('Current song now has no tags.'))
    return redirect('view_song', song_id=song.id, key=song.key)
# cart

def cart(request):
    current_user = request.user
    group = Group.objects.get(name="Minister")
    users = group.user_set.all()
    songlist = current_user.cart.all().order_by('listorder')
    context = {
        'title': _('Add event'),
        'songlist': songlist,
        'keyset': CHORDNOTE,
        'users': users,
        }
    return render(request, 'cart.html', context)

def delete_item(request, item):
    current_user = request.user 
    for i in current_user.cart.all():
        if i.id == item:
            current_user.cart.remove(i)
    return redirect('cart')        

def empty_cart(request):
    current_user = request.user
    current_user.cart.clear()
    return redirect('songbook')

def assign2event(request):
    addform = AddEventForm()
    assignform = Assign2Event()
    context = {
        'title': _('Assign to event'),
        'addform': addform,
        'assignform': assignform,
        }       
    return render(request, 'assign2event.html', context) 

def add2event(request):
    current_user = request.user
    if request.method == "POST":
        addform = AddEventForm(request.POST)
        if addform.is_valid():
            event = addform.save(commit=False)
            event.user = current_user
            event.save()
            for item in current_user.cart.all():
                event.items.add(item)
            current_user.cart.clear()
            messages.success(request, _('Success! Event is set and list added.'))
            return redirect('calendar')
        else:
            messages.error(request, _('Error! Form failed to validate.'))
            return redirect('assign2event')

def add2xevent(request):
    current_user = request.user
    if request.method == "POST":
        assignform = Assign2Event(request.POST)
        if assignform.is_valid():

            event_id = assignform.cleaned_data['title']
            event = get_object_or_404(Lists, pk=event_id)
            event_has = event.items.count()
            for item in current_user.cart.all():
                if event_has > 0:
                    initial = item.listorder
                    item.listorder = initial + event_has
                    item.save()
                event.items.add(item)
            current_user.cart.clear()
            messages.success(request, _('Success! Cart list added to event {}-{}.'.format(event.date_time, event.title)))
            return redirect('calendar')
        else:
            messages.error(request, _('Error! Form failed to validate.'))
            return redirect('assign2event')    

def add_to_cart(request, songid, c, keyword):
    song = get_object_or_404(Song, pk=songid)
    current_user = request.user
    cart = current_user.cart.all().order_by('listorder')
    
    if cart:
        lastitem = cart.last()
        if lastitem:
            lastitem_num = lastitem.listorder
        else:
            lastitem_num = 0
    else:
        lastitem_num = 0
    cartitem = ListItem(title=song.title, desired_key=song.key, listorder=lastitem_num+1)
    cartitem.save()
    
    cartitem.song.add(song)
    current_user.cart.add(cartitem)
    
    # need to finish
    if c == 1:
        return redirect('songbook')
    if c == 2:
        return redirect('songbook') # search
    else:
        return redirect('songbook') # explore

@login_required
def unsign_from_cartitem(request, item_id, username, state):
    listitem = ListItem.objects.get(pk=item_id)
    user = get_object_or_404(User, username=username)
    if user:
        listitem.assigned.remove(user)
    if state == 1:
        lists = listitem.lists.first()
        return redirect('lists', list_id = lists.id)
    if state == 2:
        return redirect('cart')

@login_required
def cart_update_list_order(request):
    if request.method == 'POST':
        order = request.POST.getlist('order[]')
        state = request.POST.get('state')
        for index, item_id in enumerate(order, start=1):
            listitem = get_object_or_404(ListItem, pk=item_id)
            listitem.listorder = index
            listitem.save()
        # return JsonResponse({'message': 'List order updated successfully.'})
        if state == 1:
            lists = listitem.lists.first()
            return redirect('lists', list_id = lists.id)
        if state == 2:
            return redirect('cart')

@login_required
def cart_update_desired_key(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        desired_key = int(request.POST.get('desired_key'))
        state = request.POST.get('state')
        list_item = get_object_or_404(ListItem, pk=item_id)
        list_item.desired_key = desired_key
        list_item.save()
        # return JsonResponse({'message': 'Desired key updated successfully.'})
        if state == 1:
            lists = list_item.lists.first()
            return redirect('lists', list_id = lists.id)
        if state == 2:
            return redirect('cart')

@login_required
def cart_update_notes(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        notes = request.POST.get('notes')
        state = request.POST.get('state')
        list_item = get_object_or_404(ListItem, pk=item_id)
        list_item.notes = notes
        list_item.save()
        # return JsonResponse({'message': 'Notes updated successfully.'})
        if state == 1:
            lists = list_item.lists.first()
            return redirect('lists', list_id = lists.id)
        if state == 2:
            return redirect('cart')

@login_required
def cart_assign_user(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user_id = request.POST.get('user_id')
        state = request.POST.get('state')
        listitem = get_object_or_404(ListItem, pk=item_id)
        user = get_object_or_404(User, pk=user_id)
        if user:
            listitem.assigned.add(user)
            listitem.save()
        if state == 1:
            lists = listitem.lists.first()
            return redirect('lists', list_id = lists.id)
        if state == 2:
            return redirect('cart')





# calendar
def calendar(request):
    # form = EmptyForm() # to delete events
    events = Lists.objects.order_by("created").all()
    for e in events:
        date = timezone.now()
        if e.date_end and e.date_end < date:  # ISSUE: Nonetype and datetime are not comparable
            e.status = 2
            e.save(update_fields=['status'])
    active_events = Lists.objects.filter(~Q(status=2))
    # check if date is passed
        
    context = {
        'title': _('Songbook'),
        'active_events': active_events,
        'lang': LANG,
    }
    return render(request, 'calendar.html', context)

def events(request):    
    events = []
    lists = Lists.objects.all()
    for list_item in lists:
        events.append({
            'id': list_item.id,
            'title': list_item.title,
            'start': list_item.date_time.strftime("%Y/%m/%d, %H:%M:%S"),
            'end': list_item.date_end.strftime("%Y/%m/%d, %H:%M:%S"),
            'url': '/lists/{}'.format(list_item.id),  # Link to the detail page
            'editable': True  # Set to False if you want to disable event editing
        })
        # event = {
        #     'id': list_item.id,
        #     'title': list_item.title,
        #     'start': list_item.date_time.isoformat() if list_item.date_time else None,  #datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        #     'end': list_item.date_end.isoformat() if list_item.date_end else None,
        #     'url': '/lists/{}'.format(list_item.id),  # Link to the detail page
        #     'editable': True  # Set to False if you want to disable event editing
        # }
        # events.append(event)
    # return jsonify(events)
    return JsonResponse(events, safe=False)

@login_required
def add_event(request):
    form = AddEventForm()
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, _('Success! Event is set.'))
            return redirect('calendar')
        else:
            messages.error(request, _('Error! Form failed to validate.'))
            return redirect(add_event)
    context = {
        'title': _('Add event'),
        'form': form,
        }
    return render(request, 'add_event.html', context)

def edit_event(request, listid):
    event = get_object_or_404(Lists, pk=listid)
    if request.method == 'POST':
        # to edit add instance of that song, otherwise a new entry will be saved instead
        form = AddEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, _('Event has been updated successfully.'))
            return redirect('lists', list_id=listid)
    else:
        context = {
            'form': AddEventForm(instance=event),
            'event': event
            }
        return render(request, 'edit_event.html', context)

def delete_event(request, eventid, jump):
    event = get_object_or_404(Lists, pk=eventid)
    if request.method == 'POST':
        event.delete()
        messages.success(request, _('Event is removed successfully.'))
        # jump to redirect based on where it has been deleted
        if jump == 1:
            return redirect('calendar')

def unsign_from_listitem(request, item_id, username, state):
    user = get_object_or_404(User, username=username)
    item = get_object_or_404(ListItem, pk=item_id)
    item.assigned.remove(user)
    listid = item.lists.first()
    return redirect('lists', list_id=listid.id)
    

def list_delete_item(request, item, listid):
    event = get_object_or_404(Lists, pk=listid)
    for i in event.items.all():
        if i.id == item:
            event.items.remove(i)
    return redirect('lists', list_id=listid)

def jall_events(request):                                                                                                 
    all_events = Lists.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'id': event.id,
            'title': event.title,
            'start': event.date_time.strftime("%Y/%m/%d, %H:%M:%S"),
            'end': event.date_end.strftime("%Y/%m/%d, %H:%M:%S"),
            'url': '/lists/{}'.format(event.id),  # Link to the detail page
            'editable': True                                                            
        })                                                                                                               
                                                                                                                     
    return JsonResponse(out, safe=False)  

def jadd_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Lists(title=str(title), date_time=start, date_end=end)
    event.save()
    data = {}
    return JsonResponse(data)


def jupdate(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Lists.objects.get(pk=id)
    event.date_time = start
    event.date_end = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)


def jremove(request):
    id = request.GET.get("id", None)
    event = Lists.objects.get(pk=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def lists(request, list_id):
    event = get_object_or_404(Lists, pk=list_id)
    de_form = EmptyForm()
    unroleform = EmptyForm()
    deleteform = EmptyForm()
    songlist = event.items.all()
    group = Group.objects.get(name="Minister")
    users = group.user_set.all()
    context = {
        'title': _('Event Details'),
        'event': event,
        'songlist': songlist,
        'keyset': CHORDNOTE,
        'users': users,
        'de_form': de_form,
        'unroleform': unroleform,
        'deleteform': deleteform,
        }
    return render(request, 'event_detail.html', context)

# on stage mode. in general three modes. lyrics with chords, lyrics, or images
def onstage(request, eventid, viewtype):
    event = get_object_or_404(Lists, pk=eventid)

    unsorted = sorted(event.items, key=lambda x: x.listorder)
    songlist = [item for item in unsorted]
    transpose = 0
    stage_mode = {}
    chords = []
    lyrics = []
    # images = []
    index_list = []
    image_state = [] # list of True false states if song has image
    music_sh = []
    if not unsorted:
        messages.error(request, _('Error, there are no items in this event.'))
        return redirect('lists', list_id=eventid)
    if not viewtype:
        messages.error(request, _('Error, view condition is not defined.'))
        return redirect('lists', list_id=eventid)
    # create two lists of lyrics with chords and without
    for i in unsorted:
        transpose = i.desired_key
        for s in i.song:
            ori_key_int = s.key
            # if song does not have chords lyrics without chords must be added.
            if s.key:
                split1 = split_text(s.lyrics, viewtype, ori_key_int, transpose) 
            else:
                split1 = split_text(s.lyrics, 2, 0, 0)    
            split2 = split_text(s.lyrics, 2, 0, 0)
        
            lyrics.append(split2)
            chords.append(split1)
            cntrl = s.image.count()
            
            if cntrl < 1:
                image_state.append(False)
            else:
                image_state.append(True)
            
    
    # create index_list and list of links of images
               
    # make a list of murls of pictures in a list
    for index, i in enumerate(unsorted):
        index_list.append(index)
        for ss in i.song:
            # create list of lists of images
            if image_state[index]:
                music_patch = []
                for i in ss.image.all():
                    music_patch.append(i)    
                music_sh.append(music_patch)
            # if no image available append chords with lyrics
            elif not image_state[index]:
                ori_key_int = ss.key
                transpose = i.desired_key
                split = split_text(ss.lyrics, 1, ori_key_int, transpose)
                music_sh.append(split) 
    
    # chords - ok
    # lyrics - ok
    # index_list - ok
    # image_state - ok
    # music_sh - ok
    
    # if viewtype == 1: # songs with chords
        
    # if viewtype == 2: # only lyrics
    #     pass
    # if viewtype == 3: # pics 
    #     pass
    stage_mode["id"]=index_list
    stage_mode["state"]=image_state
    stage_mode["chords"]=chords
    stage_mode["lyrics"]=lyrics
    stage_mode["images"]=music_sh
    
    # print(stage_mode)
    # mlinks_check = []
    # music_sh = []
    # my_dict = {}
    
    # if viewtype < 3:
    #     for i in unsorted:
    #         transpose = i.desired_key
    #         # make sure viewtype has been passed

    #         for s in i.song:
    #             ori_key_int = s.key
    #             if transpose:
    #                 split = split_text(s.lyrics, viewtype, ori_key_int, transpose)
    #             else:    
    #                 split = split_text(s.lyrics, 2, 0, 0)
    #         lyrics.append(split)
    #         # if viewtype is 3, then gather as many 
    # if viewtype == 3:
    #     # making a list of booleans if song.media has pictures or not
    #     index_list = []
    #     for i in unsorted:
    #         for s in i.song:
    #             if not s.media:
    #                 mlinks_check.append(False)
    #             else:
    #                 cntrl = 0
    #                 for m in s.media:
    #                     if m.mtype == 3:
    #                         cntrl=cntrl+1
    #                 if cntrl > 1:
    #                     mlinks_check.append(True)
    #                 else:
    #                     mlinks_check.append(False)
    #             break
                    
    #     # make a list of murls of pictures in a list
    #     for index, i in enumerate(unsorted):
                       
    #         index_list.append(index)
    #         for ss in i.song:
    #             if mlinks_check[index]:
    #                 ex = []
    #                 for ll in ss.media:
    #                     if ll.mtype ==3:
    #                         murl = ll.murl
    #                         ex.append(murl) 
    #                 music_sh.append(ex)
    #             elif mlinks_check[index] == False:
    #                 ori_key_int = ss.key
    #                 transpose = i.desired_key
    #                 split = split_text(ss.lyrics, 1, ori_key_int, transpose)
    #                 music_sh.append(split)         
    #     # make a dict
    #     my_dict["id"]= index_list
    #     my_dict["image"] = mlinks_check
    #     my_dict["values"] = music_sh 
    context = {
        'title': _('On Stage'),
        'songlist':songlist, 
        'event': event,
        'lyrics': lyrics,
        'viewtype':viewtype, 
        'stage_mode': stage_mode,
        }
    return render(request, 'onstage.html', context)