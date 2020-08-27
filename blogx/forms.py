from django import forms


class CommentForm(forms.Form):

    message = forms.CharField(max_length=200, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Comment *'}))

    name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-2',  'placeholder': 'Name (optional)'}))
