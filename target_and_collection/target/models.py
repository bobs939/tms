from django.db import models
from organization.models import Department, SubDepartment
from organization.services import RulesEngine
from django.core.exceptions import ValidationError

class Target(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        rules_engine = RulesEngine(self)
        errors = rules_engine.validate_model()
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name
