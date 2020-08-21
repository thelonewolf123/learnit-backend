from django import forms


class CommentForm(forms.Form):

    message = forms.CharField(max_length=200, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'name', 'rows': '4', 'placeholder': 'Comment *'}))
