from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.db import DatabaseError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from decimal import Decimal, ROUND_HALF_UP
from .forms import EntryForm
from .models import Entry

# View for displaying the dashboard with a list of entries and financial summaries
class DashboardView(LoginRequiredMixin, ListView):
    model               = Entry
    template_name       = "finance/dashboard.html"
    context_object_name = "entries"

    # Filter the queryset to only include entries belonging to the logged-in user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    # Add additional context data for the dashboard, including totals and balance
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        # raw sums (could be Decimal or float, depending on your DB backend)
        total_income   = qs.filter(entry_type=Entry.INCOME)  \
                           .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        total_expenses = qs.filter(entry_type=Entry.EXPENSE) \
                           .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        # ensure they’re Decimal
        total_income   = Decimal(total_income)
        total_expenses = Decimal(total_expenses)

        # quantize to exactly two decimal places
        total_income   = total_income.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_expenses = total_expenses.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # compute balance and quantize
        balance = (total_income - total_expenses).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        ctx.update({
            "total_income":   total_income,
            "total_expenses": total_expenses,
            "balance":        balance,
        })
        return ctx

# View for creating a new financial entry
class EntryCreateView(LoginRequiredMixin, CreateView):
    form_class    = EntryForm
    template_name = "finance/entry_form.html"
    success_url   = reverse_lazy("dashboard")

    # Automatically associate the new entry with the logged-in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        # Display a success message upon successful creation
        messages.success(self.request, "Entry created successfully!")
        return response

# View for deleting an existing financial entry
class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model         = Entry
    success_url   = reverse_lazy("dashboard")
