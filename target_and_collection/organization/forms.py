from django import forms
from django.forms import inlineformset_factory
from django.apps import apps
from .models import Department, SubDepartment, Rule, Condition, RuleTarget


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SubDepartmentForm(forms.ModelForm):
    class Meta:
        model = SubDepartment
        fields = ['department', 'name']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['field_name', 'operator', 'value']
        widgets = {
            'field_name': forms.TextInput(attrs={'class': 'form-control'}),
            'operator': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }

ConditionFormSet = inlineformset_factory(Rule, Condition, form=ConditionForm, extra=1, can_delete=True)


class RuleTargetForm(forms.ModelForm):
    model_name = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control model-select'}))
    field_name = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control field-select'}))

    class Meta:
        model = RuleTarget
        fields = ['rule', 'model_name', 'field_name']
        widgets = {
            'rule': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_name'].choices = self.get_model_choices()

    def get_model_choices(self):
        model_choices = []
        for model in apps.get_models():
            model_choices.append((f'{model._meta.app_label}.{model._meta.model_name}', model._meta.verbose_name.title()))
        return sorted(model_choices, key=lambda x: x[1])

RuleTargetFormSet = inlineformset_factory(Rule, RuleTarget, form=RuleTargetForm, extra=1, can_delete=True)