#-*- coding: utf-8 -*-
from casino.models import Game
from django import forms
from django.utils.translation import ugettext as _


class EntryForm(forms.ModelForm):
    """
    Form for create representation object
    """
    cached_user = None
    
    def __init__(self, *args, **kwargs):
        """
        Add user to object
        """
        if "user" in kwargs:
            self.cached_user = kwargs["user"]
            del kwargs["user"]
        super(EntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Save form model
        """
        record = super(EntryForm, self).save(commit=False)
        record.user = self.cached_user
        if commit:
            record.save()
        return record

    class Meta:
        model = Entry
        fields = ("name", "text",)

