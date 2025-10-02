from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.department.name} - {self.name}"

# Rule System Models
class Rule(models.Model):
    """
    A rule that can be applied to models to enforce validation.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Condition(models.Model):
    """
    A condition that must be met for a rule to be satisfied.
    """
    OPERATOR_CHOICES = [
        ('eq', 'Equals'),
        ('neq', 'Not Equals'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal'),
        ('contains', 'Contains'),
        ('in', 'In'),
        ('not_in', 'Not In'),
        ('belongs_to', 'Belongs To'),
    ]

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='conditions')
    field_name = models.CharField(max_length=100, help_text="The name of the field to check")
    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=255, help_text="The value to compare against")
    negate = models.BooleanField(default=False, help_text="Negate the condition")

    def __str__(self):
        return f"{self.field_name} {self.get_operator_display()} {self.value}"

class RuleTarget(models.Model):
    """
    Specifies which models or fields a rule applies to.
    """
    MODEL_CHOICES = [
        ('organization.Department', 'Department'),
        ('organization.SubDepartment', 'SubDepartment'),
        ('target.Target', 'Target'),
        ('collection.Collection', 'Collection'),
    ]

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='targets')
    model_name = models.CharField(max_length=100, choices=MODEL_CHOICES)
    field_name = models.CharField(max_length=100, blank=True, help_text="Specific field to apply rule to (leave blank for all fields)")

    def __str__(self):
        return f"{self.model_name}.{self.field_name if self.field_name else '*'}"
