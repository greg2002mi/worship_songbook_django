from django import forms
from django.db.models import F
from .models import Song, Tag, Mlinks, CHORDNOTE, Post, Audio, Image, Lists, Profile, Issues
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import os
from django.conf import settings
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

# class SetPasswordForm(PasswordChangeForm):
#     class Meta:
#         model = User
#         fields = ['new_password1', 'new_password2']


class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['name'].widget.attrs['placeholder'] = 'You can submit an issue anonymously by leaving this field blank'
        self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['title'].widget.attrs['placeholder'] = 'Generally describe your issue'
        self.fields['issue'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['issue'].widget.attrs['rows'] = '10'
        self.fields['issue'].widget.attrs['placeholder'] = 'Describe in detail an issue or error. Please also add where it happened and any additional details would be helpful'
        self.fields['contact_info'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['contact_info'].widget.attrs['placeholder'] = 'Its not required, but if provided, we may contact you for more details regarding an issue'
    
    
    class Meta:
        model = Issues
        fields = ['name', 'title', 'issue', 'contact_info']
        labels = {
            'title': _('Submit an issue'),
            'name': _('Your name'),
            'title': _('Title'),
            'issue': _('Issue'),
            'contact_info': _('Your contacts'),
        }
    
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Post
        fields = ['title', 'body']
        labels = {
            'title': _('Title'),
            'body': _('Post'),
        }

class EditPostForm(forms.ModelForm):
    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'status']
        labels = {
            'title': _('Title'),
            'body': _('Post'),
            'status': _('Status'),

        }
    

class UpdateUForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']
        
class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['mobile_no'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['mobile_no'].widget.attrs['placeholder'] = _('Phone number')
        self.fields['birthday'].widget.attrs['class'] = 'datepicker'
        self.fields['about_me'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['about_me'].widget.attrs['placeholder'] = _('Write about yourself...')
        self.fields['about_me'].widget.attrs['rows'] = '10'
    
    class Meta:
        model = Profile
        fields = ['about_me', 'mobile_no', 'birthday']
        labels = {
            'about_me': _('About_me'),
            'mobile_no': _('Mobile'),
            'birthday': _('My birthday'),
        }
        widgets = {
            "birthday": DatePickerInput(),
        }

class UploadAvatarForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar',]
        labels = {
            'avatar': _('My avatar'),
        }

class NewUForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(NewUForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class AddTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['name'].widget.attrs['placeholder'] = _('Name a new genre or tag if not in the list')  
        
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': _('Tag name')
            }

class AddSongTagForm(forms.Form):
    def __init__(self, tag, *args, **kwargs):
        super(AddSongTagForm, self).__init__(*args, **kwargs)
        # tag = Tag.objects.get(pk=tag_id)
        if tag.song:
            songs_in_tag = tag.song.all()
            songs = Song.objects.exclude(id__in=songs_in_tag.values('id'))
            
        else:
            songs = Song.objects.all()
        self.fields['song'] = forms.ModelChoiceField(queryset=songs)

class AddSongForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['title'].widget.attrs['placeholder'] = 'Write song title here'
        self.fields['singer'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['info'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['info'].widget.attrs['rows'] = '5'
        self.fields['lyrics'].widget.attrs['style'] = 'min-width: 100%, height: 400px;'
        self.fields['lyrics'].widget.attrs['id'] = 'lyrics-editor'
        self.fields['minor'].widget.attrs['type'] = 'checkbox'
        self.fields['minor'].widget.attrs['class'] = 'form-check-input'
        self.fields['singer'].widget.attrs['placeholder'] = _('Write singer or music group here')
        self.fields['info'].widget.attrs['placeholder'] = _('Any useful information, such as tempo, original key, etc.')
        self.fields['lyrics'].widget.attrs['placeholder'] = _('Write song lyrics here in chordpro format')
        self.fields['lyrics'].widget.attrs['rows'] = '15'
    
    class Meta:
        model = Song
        fields = ['title', 'singer', 'info', 'key', 'minor', 'lyrics', 'language']
        labels = {
            'title': _('Title'),
            'singer': _('Singer'),
            'info': _('Information'),
            'key': _('Key'),
            'minor': _('minor'),
            'lyrics': _('Lyrics'),
            'language': _('Language'),
        }
    

class Transpose(forms.Form):
    key = forms.CharField(label=_('Transpose'), widget=forms.Select(choices=CHORDNOTE))
    
class EditSongForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['title'].widget.attrs['placeholder'] = 'Write song title here'
        self.fields['singer'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['info'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['info'].widget.attrs['rows'] = '5'
        self.fields['lyrics'].widget.attrs['style'] = 'min-width: 100%, height: 400px;'
        self.fields['lyrics'].widget.attrs['id'] = 'lyrics-editor'
        self.fields['minor'].widget.attrs['type'] = 'checkbox'
        self.fields['minor'].widget.attrs['class'] = 'form-check-input'
        self.fields['singer'].widget.attrs['placeholder'] = _('Write singer or music group here')
        self.fields['info'].widget.attrs['placeholder'] = _('Any useful information, such as tempo, original key, etc.')
        self.fields['lyrics'].widget.attrs['placeholder'] = _('Write song lyrics here in chordpro format')
        self.fields['lyrics'].widget.attrs['rows'] = '15'
    
    class Meta:
        model = Song
        fields = ['title', 'singer', 'info', 'key', 'minor', 'lyrics', 'language', 'status']
        labels = {
            'title': _('Title'),
            'singer': _('Singer'),
            'info': _('Information'),
            'key': _('Key'),
            'minor': _('minor'),
            'lyrics': _('Lyrics'),
            'language': _('Language'),
            'status': _('Status'),
        }

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# class TransSongForm(forms.Form):
#     tr_song_id = forms.ModelChoiceField(queryset=Song.objects.exclude(language=F('song__language')).exclude(translation__id=F('id')), label='Translated Song')

class TagsForm(forms.Form):
    name = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,)
    # name = forms.MultipleChoiceField(label='Tags', widget=forms.CheckboxSelectMultiple(attrs={'name': 'tags'}))
    # name = forms.MultipleChoiceField(label='Tags', choices=[(tag.id, tag.name) for tag in Tag.objects.all()], widget=forms.CheckboxSelectMultiple(attrs={'name': 'tags'}))
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)  # Retrieve the 'choices' argument, if provided
        super(TagsForm, self).__init__(*args, **kwargs)
    
# class TagsForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ('name',)
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Make the query here
#         MYQUERY = Tag.objects.values_list('id', 'name')
#         self.fields['name'] = forms.ChoiceField(choices=(*MYQUERY,))
    # name = forms.MultipleChoiceField(label='Tags', choices=[(choice.pk, choice) for choice in Tag.objects.all()], widget=forms.CheckboxSelectMultiple)
    
    
class AddMediaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['filename'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['filename'].widget.attrs['placeholder'] = _('Title of a video or type Youtube')
        self.fields['murl'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['murl'].widget.attrs['placeholder'] = _('Paste embed url link, taken from desired youtube clip')
        
    class Meta:
        model = Mlinks
        fields = ['filename', 'murl']
        labels = {
            'filename': _('File name'),
            'murl': _('URL'),
        }

# class AddAudioForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#         self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
#         self.fields['title'].widget.attrs['placeholder'] = _('Title of audio')
        
#     class Meta:
#         model = Audio
#         fields = ['title']
#         labels = {
#             'title': _('Title'),

#         }

        
class SongsForm(forms.Form):
    title = forms.ChoiceField(choices=[])
        
    def __init__(self, *args, current_song=None, **kwargs):
        super().__init__(*args, **kwargs)

        if current_song:
            print(current_song.title)
            # Filter songs based on language and exclude the current song
            MYQUERY = Song.objects.exclude(
                language=current_song.language
            ).values_list('id', 'title')
        else:
            # Default query when no current_song is provided
            MYQUERY = Song.objects.values_list('id', 'title')

        self.fields['title'] = forms.ChoiceField(choices=MYQUERY)
        self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['title'].widget.attrs['class'] = 'form-control'
    # to make a dropdown list choices populated from model 
    # choice = forms.ModelChoiceField(label='Songs', queryset=Song.objects.filter(language=1), required=True)
    
class EmptyForm(forms.Form):
    pass

class AddEventForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['title'].widget.attrs['placeholder'] = _('Sunday service, Morning Prayer, Prayer and Worship service etc.')
        self.fields['mlink'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['mlink'].widget.attrs['rows'] = '3'
        self.fields['mlink'].widget.attrs['placeholder'] = _('Link from Youtube. Embed links only')
        self.fields['date_time'].widget.attrs['class'] = 'datetimepicker'
        self.fields['date_end'].widget.attrs['class'] = 'datetimepicker'
        self.fields['passage'].widget.attrs['style'] = 'min-width: 100%'
        self.fields['passage'].widget.attrs['placeholder'] = _('Slogans, Theme of service, Bible verse, etc.')
        self.fields['passage'].widget.attrs['rows'] = '15'
        
    class Meta:
        model = Lists
        fields = ['title', 'date_time', 'date_end', 'mlink', 'passage', 'status']
        labels = {
            'title': _('Title'),
            'date_time': _('Start date'),
            'date_end': _('till'),
            'mlink': _('Media Link'),
            'passage': _('Bible passage'),
            'status': _('Status'),
        }
        widgets = {
            "date_end": DateTimePickerInput(),
            "date_time": DateTimePickerInput(),
        }

# class Assign2Event(forms.Form):
#     class Meta:
#         fields = ('title',)
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Make the query here
#         MYQUERY = Lists.objects.values_list('id', 'title')
#         self.fields['title'] = forms.ChoiceField(choices=(*MYQUERY,))

class Assign2Event(forms.Form):
    title = forms.ChoiceField()
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the query here
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        my_query = Lists.objects.values_list('id', 'title', 'date_time')
        choices = [('', '---------')]  # Add an empty choice for the default selection

        for item_id, title, date_time in my_query:
            # Format the date_time value to display in the dropdown
            formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M')
            choice_label = f"{formatted_date_time} - {title}"
            choices.append((item_id, choice_label))

        self.fields['title'].choices = choices
