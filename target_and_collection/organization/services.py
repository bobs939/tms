from django.apps import apps
from organization.models import Rule, Condition, RuleTarget

class RulesEngine:
    """
    A service class that interprets and validates rules dynamically.
    """
    
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.model_name = f"{model_instance._meta.app_label}.{model_instance._meta.model_name}"
    
    def get_applicable_rules(self):
        """
        Returns all active rules that apply to this model instance.
        """
        return Rule.objects.filter(
            is_active=True,
            targets__model_name=self.model_name
        ).distinct()
    
    def evaluate_condition(self, condition, field_value):
        """
        Evaluates a single condition against a field value.
        Returns True if the condition is satisfied, False otherwise.
        """
        condition_value = condition.value
        
        # Convert numeric values if possible
        try:
            if isinstance(field_value, (int, float)):
                condition_value = float(condition_value)
        except (ValueError, TypeError):
            pass
        
        # Evaluate the condition based on the operator
        result = False
        
        if condition.operator == 'eq':
            result = field_value == condition_value
        elif condition.operator == 'neq':
            result = field_value != condition_value
        elif condition.operator == 'gt':
            result = field_value > condition_value
        elif condition.operator == 'gte':
            result = field_value >= condition_value
        elif condition.operator == 'lt':
            result = field_value < condition_value
        elif condition.operator == 'lte':
            result = field_value <= condition_value
        elif condition.operator == 'contains':
            result = condition_value in str(field_value)
        elif condition.operator == 'in':
            result = field_value in condition_value.split(',')
        elif condition.operator == 'not_in':
            result = field_value not in condition_value.split(',')
        elif condition.operator == 'belongs_to':
            # For belongs_to, we expect condition_value to be a model name
            related_model = apps.get_model(condition_value)
            result = field_value in related_model.objects.all()
        
        return not result if condition.negate else result
    
    def validate_field(self, field_name, field_value):
        """
        Validates a specific field against all applicable rules.
        Returns a list of error messages for failed rules.
        """
        errors = []
        
        for rule in self.get_applicable_rules():
            # Check if this rule applies to this specific field
            if not rule.targets.filter(
                model_name=self.model_name,
                field_name__in=['', field_name]
            ).exists():
                continue
            
            # Check all conditions for this rule
            conditions_met = all(
                self.evaluate_condition(
                    condition,
                    getattr(self.model_instance, condition.field_name, None)
                )
                for condition in rule.conditions.all()
            )
            
            if not conditions_met:
                errors.append(f"Field '{field_name}' violates rule: {rule.name}")
        
        return errors
    
    def validate_model(self):
        """
        Validates the entire model instance against all applicable rules.
        Returns a dictionary of field names to lists of error messages.
        """
        errors = {}
        
        for rule in self.get_applicable_rules():
            # Get all fields this rule applies to
            target_fields = rule.targets.filter(
                model_name=self.model_name
            ).values_list('field_name', flat=True)
            
            # If rule applies to specific fields, check only those
            if target_fields and '' not in target_fields:
                for field_name in target_fields:
                    field_errors = self.validate_field(field_name, getattr(self.model_instance, field_name, None))
                    if field_errors:
                        errors.setdefault(field_name, []).extend(field_errors)
            else:
                # Rule applies to all fields - check all fields
                for field in self.model_instance._meta.get_fields():
                    if field.is_relation or field.name in ['id', 'pk']:
                        continue
                    
                    field_errors = self.validate_field(field.name, getattr(self.model_instance, field.name, None))
                    if field_errors:
                        errors.setdefault(field.name, []).extend(field_errors)
        
        return errors