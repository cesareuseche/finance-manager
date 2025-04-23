from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Entry
from .utils import dump_entries_to_files
from django.contrib import messages

# -----------------------------------------------------------------------------
# Whenever an Entry is created/updated (post_save) or deleted (post_delete),
# Django will call this function to keep your on-disk dumps in sync.
# -----------------------------------------------------------------------------
@receiver([post_save, post_delete], sender=Entry)
def sync_files(sender, **kwargs):
    """
    Signal handler that fires after an Entry is saved or deleted.
    It calls dump_entries_to_files() to regenerate JSON/CSV dumps.
    """
    try:
        # Read all Entry objects and rewrite your data files
        dump_entries_to_files()
    except Exception as e:
        # If something goes wrong, attempt to notify via Django’s messages framework.
        # Note: messages.error normally requires a request object, so passing None
        # here won’t display in the UI—but the intent is to capture/report errors.
        messages.error(None, f"Error syncing files: {e}")
