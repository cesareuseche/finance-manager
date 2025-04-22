from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Entry

User = get_user_model()

class EntryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pass")

    def _make_entry(self, **kwargs):
        """Helper to build an Entry without saving."""
        data = {
            "user": self.user,
            "entry_type": Entry.INCOME,
            "source": "Salary",
            "description": "",
            "category": "",
            "amount": Decimal("100.00"),
            "date": date.today(),
        }
        data.update(kwargs)
        return Entry(**data)

    def test_valid_income_passes_validation(self):
        e = self._make_entry()
        # Should not raise
        e.full_clean()

    def test_negative_amount_raises(self):
        e = self._make_entry(amount=Decimal("-1.00"))
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("amount", cm.exception.error_dict)

    def test_future_date_raises(self):
        future = date.today() + timedelta(days=1)
        e = self._make_entry(date=future)
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("date", cm.exception.error_dict)
        self.assertEqual(
            cm.exception.error_dict["date"][0].code,
            "date_future"
        )

    def test_income_without_source_raises(self):
        e = self._make_entry(entry_type=Entry.INCOME, source="")
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("source", cm.exception.error_dict)
        self.assertEqual(
            cm.exception.error_dict["source"][0].code,
            "source_required"
        )

    def test_expense_without_category_raises(self):
        e = self._make_entry(entry_type=Entry.EXPENSE, source="", category="")
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("category", cm.exception.error_dict)
        self.assertEqual(
            cm.exception.error_dict["category"][0].code,
            "category_required"
        )

    def test_display_helpers_return_verbose_labels(self):
        inc = self._make_entry(entry_type=Entry.INCOME)
        exp = self._make_entry(entry_type=Entry.EXPENSE, category="food")
        self.assertEqual(inc.get_entry_type_display(), "Income")
        self.assertEqual(exp.get_entry_type_display(), "Expense")
        self.assertEqual(exp.get_category_display(), "Food")

    def test_str_shows_type_and_amount(self):
        e = self._make_entry(entry_type=Entry.EXPENSE, amount=Decimal("42.50"))
        # Check the string representation
        self.assertEqual(str(e), "Income - 42.50")
        # and for an expense…
        e.entry_type = Entry.EXPENSE
        self.assertEqual(str(e), "Expense - 42.50")
