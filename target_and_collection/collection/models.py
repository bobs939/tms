from django.db import models
from organization.models import Department, SubDepartment
from organization.services import RulesEngine


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def clean(self):
        rules_engine = RulesEngine(self)
        rules_engine.validate_model()

    def __str__(self):
        return self.name
