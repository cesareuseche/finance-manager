from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Entry

class EntryModelTests(TestCase):
    def setUp(self):
        self.u = get_user_model().objects.create_user("alice", password="pass")

    def test_add_income_and_expense(self):
        inc = Entry.objects.create(
            user=self.u, entry_type=Entry.INCOME,
            source="Salary", amount=1000, date="2025-04-01")
        exp = Entry.objects.create(
            user=self.u, entry_type=Entry.EXPENSE,
            description="Rent", category="Housing",
            amount=400, date="2025-04-02")

        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(inc.amount + exp.amount, Decimal("1400"))

    def test_negative_amount_rejected(self):
        with self.assertRaises(Exception):
            Entry.objects.create(
                user=self.u, entry_type=Entry.INCOME,
                source="Bad", amount=-10, date="2025-04-01")
