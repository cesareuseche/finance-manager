# 💰 Personal Finance Manager (Django 5)

A minimalist, self‑hosted web app that lets you track income and expenses, see running totals, and export your data.
Built as a learning project for the PRG 402 syllabus and tested on macOS (Apple Silicon) & Linux.

---

## ✨ Core Features

| Feature | Details |
|---------|---------|
| **Add & Manage Entries** | Enter income (source + amount) and expenses (description, category, amount, date). Create and delete entries as needed. |
| **Per‑User Dashboard** | Each authenticated user sees only their own data with totals for income, expenses, and calculated balance. |
| **File Persistence** | Every create/update/delete automatically dumps JSON (`data/finance_data.json`) and a CSV‑like text file (`data/finance_data.txt`) via Django signals. |
| **Validation & Errors** | Server‑side validation for positive amounts, required fields based on entry type, and date validation. Clear form error messages. |
| **Authentication** | Django's built-in authentication with custom signup view; `LoginRequiredMixin` protects all finance views. |
| **Unit Tests** | `finance/tests.py` covers model validation & basic calculations. |

---

## 🛠️ Tech Stack

- **Python 3.13** (works on 3.10+)
- **Django 5.2**
- SQLite (default) for database storage
- Django's built-in test framework
- `python-dotenv` for `.env` configuration
- SCSS/Sass for styling (via npm packages)

---

## 🚀 Local Setup (macOS/Linux/Windows)

```bash
# 1 ⃣ Clone & enter
git clone https://github.com/<your‑user>/finance-manager.git
cd finance-manager

# 2 ⃣ Create virtual‑env (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# 3 ⃣ Install deps
pip install -r requirements.txt

# 4 ⃣ Environment vars
# Create a .env file manually with:
#   SECRET_KEY=django-insecure-<random-string>
#   DEBUG=True

# 5 ⃣ DB setup
python manage.py migrate
python manage.py createsuperuser     # follow prompts

# 6 ⃣ Run!
python manage.py runserver
# Browse http://127.0.0.1:8000/

# Optional: Build CSS from SCSS
npm install
npm run build:css
