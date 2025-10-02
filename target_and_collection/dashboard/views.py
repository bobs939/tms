from django.shortcuts import render
from collection.models import Collection
from organization.models import Department, SubDepartment, Rule
from target.models import Target
from django.db.models import Count

def dashboard_view(request):
    # Total Counts
    total_departments = Department.objects.count()
    total_subdepartments = SubDepartment.objects.count()
    total_targets = Target.objects.count()
    total_collections = Collection.objects.count()
    total_rules = Rule.objects.count()

    # Collections by Department
    collections_by_department = Collection.objects.values('department__name').annotate(count=Count('id'))
    collections_labels = [item['department__name'] if item['department__name'] else 'No Department' for item in collections_by_department]
    collections_data = [item['count'] for item in collections_by_department]

    # Targets by Department
    targets_by_department = Target.objects.values('department__name').annotate(count=Count('id'))
    targets_labels = [item['department__name'] if item['department__name'] else 'No Department' for item in targets_by_department]
    targets_data = [item['count'] for item in targets_by_department]

    # Rules Status (Active vs Inactive)
    rules_status = Rule.objects.values('is_active').annotate(count=Count('id'))
    rules_labels = ["Active" if item['is_active'] else "Inactive" for item in rules_status]
    rules_data = [item['count'] for item in rules_status]

    context = {
        'total_departments': total_departments,
        'total_subdepartments': total_subdepartments,
        'total_targets': total_targets,
        'total_collections': total_collections,
        'total_rules': total_rules,
        'collections_labels': collections_labels,
        'collections_data': collections_data,
        'targets_labels': targets_labels,
        'targets_data': targets_data,
        'rules_labels': rules_labels,
        'rules_data': rules_data,
    }
    return render(request, 'dashboard/dashboard.html', context)
