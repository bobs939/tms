from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.apps import apps
from .models import Department, SubDepartment, Rule, Condition, RuleTarget
from .forms import DepartmentForm, SubDepartmentForm, RuleForm, ConditionForm, RuleTargetForm, ConditionFormSet, RuleTargetFormSet


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'organization/department_list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'organization/department_form.html', {'form': form})


def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('organization:department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'organization/department_form.html', {'form': form})


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('organization:department_list')
    return render(request, 'organization/department_confirm_delete.html', {'department': department})


def subdepartment_list(request):
    subdepartments = SubDepartment.objects.all()
    return render(request, 'organization/subdepartment_list.html', {'subdepartments': subdepartments})


def subdepartment_create(request):
    if request.method == 'POST':
        form = SubDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization:subdepartment_list')
    else:
        form = SubDepartmentForm()
    return render(request, 'organization/subdepartment_form.html', {'form': form})


def subdepartment_update(request, pk):
    subdepartment = get_object_or_404(SubDepartment, pk=pk)
    if request.method == 'POST':
        form = SubDepartmentForm(request.POST, instance=subdepartment)
        if form.is_valid():
            form.save()
            return redirect('organization:subdepartment_list')
    else:
        form = SubDepartmentForm(instance=subdepartment)
    return render(request, 'organization/subdepartment_form.html', {'form': form})


def subdepartment_delete(request, pk):
    subdepartment = get_object_or_404(SubDepartment, pk=pk)
    if request.method == 'POST':
        subdepartment.delete()
        return redirect('organization:subdepartment_list')
    return render(request, 'organization/subdepartment_confirm_delete.html', {'subdepartment': subdepartment})


def rule_list(request):
    rules = Rule.objects.all()
    return render(request, 'organization/rule_list.html', {'rules': rules})


def rule_create(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        condition_formset = ConditionFormSet(request.POST, instance=Rule())
        rule_target_formset = RuleTargetFormSet(request.POST, instance=Rule())
        if form.is_valid() and condition_formset.is_valid() and rule_target_formset.is_valid():
            rule = form.save()
            condition_formset.instance = rule
            condition_formset.save()
            rule_target_formset.instance = rule
            rule_target_formset.save()
            return redirect('organization:rule_list')
    else:
        form = RuleForm()
        condition_formset = ConditionFormSet(instance=Rule())
        rule_target_formset = RuleTargetFormSet(instance=Rule())
    return render(request, 'organization/rule_form.html', {
        'form': form,
        'condition_formset': condition_formset,
        'rule_target_formset': rule_target_formset
    })


def rule_update(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == 'POST':
        form = RuleForm(request.POST, instance=rule)
        condition_formset = ConditionFormSet(request.POST, instance=rule)
        rule_target_formset = RuleTargetFormSet(request.POST, instance=rule)
        if form.is_valid() and condition_formset.is_valid() and rule_target_formset.is_valid():
            form.save()
            condition_formset.save()
            rule_target_formset.save()
            return redirect('organization:rule_list')
    else:
        form = RuleForm(instance=rule)
        condition_formset = ConditionFormSet(instance=rule)
        rule_target_formset = RuleTargetFormSet(instance=rule)
    return render(request, 'organization/rule_form.html', {
        'form': form,
        'condition_formset': condition_formset,
        'rule_target_formset': rule_target_formset
    })


def rule_delete(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == 'POST':
        rule.delete()
        return redirect('organization:rule_list')
    return render(request, 'organization/rule_confirm_delete.html', {'rule': rule})

def get_model_fields(request):
    model_name = request.GET.get('model_name')
    app_label, model_name = model_name.split('.')
    try:
        model = apps.get_model(app_label, model_name)
        fields = []
        for field in model._meta.get_fields():
            if hasattr(field, 'verbose_name'):
                fields.append({'name': field.name, 'verbose_name': field.verbose_name})
            else:
                fields.append({'name': field.name, 'verbose_name': field.name})
        return JsonResponse(fields, safe=False)
    except LookupError:
        return JsonResponse([], safe=False)
