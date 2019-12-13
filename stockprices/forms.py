
from django import forms
 
class PostForm(forms.Form):
    start = forms.DateField(label = "Start (yyyy-mm-dd):")
    end = forms.DateField(label = "End (yyyy-mm-dd):")
    tickers = forms.CharField(widget=forms.Textarea, label = "(Yahoo) Tickers (separate with spaces):")
    periodicity = forms.ChoiceField(choices=[("1mo",'Monthly'), ("1wk", 'Weekly'), ("1d", 'Daily')])


