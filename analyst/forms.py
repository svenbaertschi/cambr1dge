from django import forms
 
class Options(forms.Form):
    procedure = forms.ChoiceField(choices=[("markowitz",'Markowitz Frontiers'), ("correlation", 'Correlations'), ("covariance", 'Covariances')])