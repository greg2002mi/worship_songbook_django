from django import forms
from .models import Song, Tag, Mlinks, CHORDNOTE, Profile, Post
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import os
from django.conf import settings


class UpdateUForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']
        
class UpdateProfileForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    mobile_no = PhoneNumberField()
    birthday = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['about_me', 'mobile_no', 'birthday']
        labels = {
            'about_me': _('About_me'),
            'mobile_no': _('Mobile'),
            'birthday': _('My birthday'),
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


class TagsForm(forms.Form):
    name = forms.MultipleChoiceField(label='Tags', choices=[(tag.id, tag.name) for tag in Tag.objects.all()], widget=forms.CheckboxSelectMultiple(attrs={'name': 'tags'}))

    
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
    class Meta:
        model = Mlinks
        fields = ['filename', 'murl']
        labels = {
            'filename': _('File name'),
            'murl': _('URL'),
        }
        
class SongsForm(forms.Form):
    class Meta:
        fields = ('title',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the query here
        MYQUERY = Song.objects.values_list('id', 'title')
        self.fields['title'] = forms.ChoiceField(choices=(*MYQUERY,))
    
    # to make a dropdown list choices populated from model 
    # choice = forms.ModelChoiceField(label='Songs', queryset=Song.objects.filter(language=1), required=True)
    
class EmptyForm(forms.Form):
    pass