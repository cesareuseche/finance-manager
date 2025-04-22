from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

# Here we define the models for the finance app.
# The Entry model represents a financial entry (either income or expense).
# The Category model represents a category for the financial entries.
class Entry(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    FOOD = 'food'
    TRANSPORT = 'transport'
    ENTERTAINMENT = 'entertainment'
    SALARY = 'salary'
    OTHER = 'other'
    CATEGORY_CHOICES = [
        (FOOD, 'Food'),
        (TRANSPORT, 'Transport'),
        (ENTERTAINMENT, 'Entertainment'),
        (SALARY, 'Salary'),
        (OTHER, 'Other'),
    ]

    # Here we are defining the fields for the Entry model.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    source = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Here the meta class is defined to set the ordering of the entries by date in descending order.
    class Meta:
        ordering = ['-date']

    # Here we define the string representation of the Entry model.
    # It returns the entry type and amount.
    def __str__(self):
       return f"{self.get_entry_type_display()} - {self.amount}"