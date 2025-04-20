from django import forms
import datetime
from .models import Entry

class EntryForm(forms.ModelForm):
    """
    Form for creating/updating Entry instances.
    Validates:
      • income must have a source
      • expense must have a category
      • amount > 0
      • date is not in the future
    """
    error_messages = {
        "source_required": "Select a valid choice. “%(value)s” is not one of the available choices.",
        "category_required": "Category is required for expense entries.",
        "amount": "Amount must be greater than zero.",
        "date_future": "Date cannot be in the future.",
        "date_past": "Date cannot be in the past.",
        "date": "Date must be in the format MM-DD-YYYY.",
        "required": "This field is required.",
    }

    class Meta:
        model  = Entry
        fields = ["entry_type", "source", "description",
                  "category", "amount", "date"]

    def clean(self):
        cleaned = super().clean()
        entry_type = cleaned.get("entry_type")

        if entry_type == Entry.INCOME and not cleaned.get("source"):
            raise forms.ValidationError(
                self.error_messages["source_required"] % {
                    "value": cleaned.get("source") or "—"
                }
            )

        if entry_type == Entry.EXPENSE and not cleaned.get("category"):
            raise forms.ValidationError(self.error_messages["category_required"])

        amount = cleaned.get("amount")
        if amount is not None and amount <= 0:
            raise forms.ValidationError(self.error_messages["amount"])

        date = cleaned.get("date")
        if date and date > datetime.date.today():
            raise forms.ValidationError(self.error_messages["date"])

        if date and date < datetime.date.today():
            raise forms.ValidationError(self.error_messages["date_past"])
        try:
            datetime.datetime.strptime(date, "%m-%d-%Y")
        except ValueError:
            raise forms.ValidationError(self.error_messages["date"])
        if not date:
            raise forms.ValidationError(self.error_messages["required"])

        return cleaned
