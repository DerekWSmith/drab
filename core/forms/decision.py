# forms/decision.py
from django import forms
from core.models.Decision import Decision

class DecisionForm(forms.ModelForm):
    '''
    Because created_at is defined in the abstract base class with auto_now_add=True,
    Django sets editable=False automatically. This means:
	•	It’s excluded from modelforms by default.
	•	Even fields = '__all__' will skip it.

    To include it, it must be explicitly redeclared in the form, like:
    '''

    # created_at = forms.DateTimeField(required=False)
    # referenced_at = forms.DateTimeField(required=False)
    # updated_at = forms.DateTimeField(required=False)


    class Meta:
        model = Decision
        fields = '__all__'


        widgets = {
            'created_at': forms.DateTimeInput(attrs={'readonly': True, 'disabled': True, 'class': 'form-control'}),
            'referenced_at': forms.DateTimeInput(attrs={'readonly': True, 'disabled': True, 'class': 'form-control'}),
            'updated_at': forms.DateTimeInput(attrs={'readonly': True, 'disabled': True, 'class': 'form-control'}),
            'adopted_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'publish_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'publish_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }