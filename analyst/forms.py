from django import forms
 
class Options(forms.Form):
    procedure = forms.ChoiceField(choices=[("pca", 'Principal Component Analysis'), ("markowitz",'Markowitz Efficient Frontiers'), ("corrcov", 'Correlations/Covariances')])