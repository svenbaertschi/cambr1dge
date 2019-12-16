from django import forms
 
class Options(forms.Form):
    procedure = forms.ChoiceField(choices=[("markowitz",'Markowitz Efficient Frontiers'), ("corrcov", 'Correlations/Covariances'), ("pca", 'Principal Component Analysis')])