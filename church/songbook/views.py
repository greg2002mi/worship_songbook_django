from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.paginator import (EmptyPage, PageNotAnInteger,
Paginator)
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post, Mlinks, Tag, Song, Lists, ListItem, Image, LANG, CHORDNOTE
from django.utils.translation import gettext as _
from .forms import AddSongForm, Transpose, AddTagForm, TagsForm, SongsForm, EmptyForm, EditSongForm, NewUForm, UpdateUForm, UpdateProfileForm
from .core import Chordpro_html
from django import forms
import os
from django.contrib import messages
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

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
    if request.method == 'POST':
        user_form = UpdateUForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'user.html', {'user_form': user_form, 'profile_form': profile_form})

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

   
def songbook(request):
    
    songs = Song.objects.filter(status=1).order_by('title')
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
        # 'next_url': next_url,
        # 'prev_url': prev_url,
        'keyset': CHORDNOTE,
        'lang': LANG,
        'form': form,
        'tags': tags,
        'page_obj': page_obj,
    }
    return render(request, 'songbook.html', context)
 
def add_song(request):
    if request.method == 'POST':
        form = AddSongForm(request.POST)
        if form.is_valid():
            saved_form = form.save()
            song_id = saved_form.pk
            key = saved_form.key
            messages.success(request, _("Song successfully add as a draft."))
            return redirect('view_song', song_id=song_id, key=key)  # Redirect to the songbook page after successful submission
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
    images = Image.objects.filter(song=song_id).all()
    media = song.media.all()
    tagged_list = ()
    tag_states = {}
    # if song.tags:
    #     tagged_list = ([tagged.name for tagged in song.tags])
    # ori_key = ''
    ori_key_int = song.key
    lyrics = song.lyrics
    # upload files
    media_root = settings.MEDIA_ROOT
    # directory = os.path.join(media_root, 'photos')
    files = os.listdir(media_root)
    
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
    # t1_songlist = song.translated.order_by(Song.title).all()
    # t2_songlist = song.translation.order_by(Song.title).all()
    # t_songlist = list(t1_songlist)
    # for song_obj in t2_songlist:
    #     if song_obj not in t_songlist:
    #         t_songlist.append(song_obj)
    delete_form = EmptyForm()
    tags_form = TagsForm()
    # populate choices for tags_form from db
    # choices = [(t.id, t.name) for t in tags]
    # tags_form.name.choices = choices
    # print(choices)
    if key is None:
        transpose = ori_key_int
    else: 
        transpose = int(key)
    # to send original key as string
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
            form = Transpose(request.POST)
            if form.is_valid():
                # Handle the submit of transpose chord action
                key = form.cleaned_data['key']
                return redirect('view_song', song_id=song.id, key=key)
        elif request.method == 'GET':
            key_dict = {'key': key}
            for tag in tags:
                tag_states[tag.id] = tag in song.tags
                
            context = {
                'title': _('View Song'),
                'song': song,
                'keyset': CHORDNOTE,
                'lang': LANG,
                'tags': tags,
                'html': html, 
                'transl_form': transl_form, 
                'remove_transl_form': remove_transl_form, 
                'delete_form': delete_form, 
                'tagged_list': tagged_list, 
                'tag_states': tag_states, 
                'tags_form': tags_form, 
                'only_lyrics': only_lyrics, 
                'form': Transpose(initial=key_dict), 
                'ori_key': ori_key, 
                # 't_songlist': t_songlist,  
                'untagall_form': untagall_form, 
                'media': media,
                'images': images,
                'files': files,
                
            }
    
    return render(request, 'view_song.html', context)

def delete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    # delete song from database
    return redirect('songbook')

def edit_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        form = EditSongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Song has been updated successfully.'))
            return redirect('view_song', song_id=song_id)
    else:
        context = {
            'form': EditSongForm(instance=song),
            'song_id': song_id, 
            'song': song,
            }
        return render(request, 'edit_song.html', context)

def upload_audio(request, song_id, mtype):
    pass

def file_upload(request, song_id, mtype):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        media = song.image.all()
        num = len(media) + 1
        newname = "{}.image_{}.jpg".format(song.id, str(num))
        my_file.name = newname # change name of image
        Image.objects.create(image=my_file, song=song, filename=newname)
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
    pass

def upload_i(request, filename):
    pass

def add_transl(request, song_id):
    pass

def remove_transl(request, selsong_id, cursong_id):
    pass

def tagging(request, song_id):
    pass

def untagall(request, song_id):
    pass