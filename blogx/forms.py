from django import forms


class CommentForm(forms.Form):

    comment= forms.CharField(max_length=200, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Subject *'}))