from django import forms
from .models import topic,post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Whats on your Mind ?'}),
                              max_length=4000,
                              help_text='The max length of the text is 4000.',
                             )

    class Meta:
        model = topic
        fields = ['subject', 'message']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['message']



