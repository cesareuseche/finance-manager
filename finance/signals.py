from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Entry
from .utils import dump_entries_to_files
from django.contrib import messages

@receiver([post_save, post_delete], sender=Entry)
def sync_files(sender, **kwargs):
    try:
        dump_entries_to_files()
    except Exception as e:
        messages.error(None, f"Error syncing files: {e}")
