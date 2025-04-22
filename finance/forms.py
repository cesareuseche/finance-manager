from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Entry
import datetime

class EntryForm(forms.ModelForm):
    """
    Form for creating/updating Entry instances.
    Validates:
      • income must have a source
      • expense must have a category
      • amount > 0
      • date is not in the future
    """
    entry_type = forms.ChoiceField(
        choices=[('', 'Select entry type')] + Entry.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'your-input-class'}),
        error_messages={'required': 'Please choose an entry type.'}
    )

    category = forms.ChoiceField(
        required=False,
        choices=[('', 'Select a category')] + Entry.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'your-input-class'}),
        error_messages={'required': 'Please choose a category.'}
    )

    error_messages = {
        "source_required": "Select a valid choice. “%(value)s” is not one of the available choices.",
        "category_required": "Category is required for expense entries.",
        "amount": "Amount must be greater than zero.",
        "date_future": "Date cannot be in the future.",
        "date": "Date must be in the format MM-DD-YYYY.",
        "required": "This field is required.",
    }

    class Meta:
        model  = Entry
        fields = ["entry_type", "source", "description",
                  "category", "amount", "date"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "aria-invalid": "false",
                    "class": "your-input-class"
                },
                format="%Y-%m-%d",
            ),
        }

    def clean(self):
        cleaned = super().clean()
        entry_type = cleaned.get("entry_type")

        # income must have source
        if entry_type == Entry.INCOME and not cleaned.get("source"):
            self.add_error(
                "source",
                ValidationError(
                    self.error_messages["source_required"] % {
                        "value": cleaned.get("source") or "Select a source"
                    },
                    code="source_required"
                )
            )

        # expense must have category
        if entry_type == Entry.EXPENSE and not cleaned.get("category"):
            self.add_error(
                "category",
                ValidationError(
                    self.error_messages["category_required"] % {
                        "value": cleaned.get("category") or "Select a category"
                    },
                    code="category_required"
                )
            )

        # amount > 0
        amount = cleaned.get("amount")
        if amount is not None and amount <= 0:
            self.add_error("amount", self.error_messages["amount"])

        # date handling
        date_val = cleaned.get("date")
        if not date_val:
            self.add_error("date", self.error_messages["required"])
            return cleaned

        # if a string was passed (unlikely with a DateField), try parsing
        if isinstance(date_val, str):
            try:
                parsed_dt = datetime.datetime.strptime(date_val, "%m-%d-%Y")
                date_val = parsed_dt.date()
            except (ValueError, TypeError):
                self.add_error("date", self.error_messages["date"])
                return cleaned

        # now date_val should be a date
        today = timezone.localdate()

        if date_val > today:
            self.add_error("date", self.error_messages["date_future"])

        # write back the cleaned date if we parsed it
        cleaned["date"] = date_val

        return cleaned