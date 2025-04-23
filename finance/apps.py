from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finance"

    def ready(self):
        """
        Code in here runs *after* the app registry is fully populated,
        so it's safe to import models, connect signals, or load seed data.
        """
        # 1. connect signals
        from . import signals          # noqa: F401  (import just for side‑effects)

        # 2. optional: load JSON seed data if DB empty
        self._load_seed_data()

    # ------------------------------------------------------------------
    # Helper method lives inside the class so it can be called from ready()
    # ------------------------------------------------------------------
    def _load_seed_data(self):
        import json
        from pathlib import Path
        from django.conf import settings
        from django.db.utils import OperationalError, ProgrammingError
        from .models import Entry
        from .utils import JSON_FILE

        # skip if migrations haven't run yet (or during 'makemigrations')
        try:
            if JSON_FILE.exists() and not Entry.objects.exists():
                data = json.loads(Path(JSON_FILE).read_text())
                for row in data:
                    row.pop("id", None)
                    Entry.objects.get_or_create(**row)
        except (OperationalError, ProgrammingError):
            pass
