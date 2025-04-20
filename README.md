# 💰 Personal Finance Manager (Django 5)

A minimalist, self‑hosted web app that lets you track income and expenses, see running totals, and export your data.
Built as a learning project for the PRG 402 syllabus and tested on macOS (Apple Silicon) & Linux.

---

## ✨ Core Features

| Feature | Details |
|---------|---------|
| **Add & Manage Entries** | Enter income (source + amount) and expenses (description, category, amount, date). Edit or delete anytime. |
| **Per‑User Dashboard** | Each authenticated user sees only their own data with totals for income, expenses, and remaining balance. |
| **File Persistence** | Every create/update/delete automatically dumps JSON (`data/finance_data.json`) and a CSV‑like text file (`data/finance_data.txt`) for offline backup. |
| **Validation & Errors** | Server‑side checks for negative amounts, missing required fields, and future‑dated transactions. Helpful form errors, no crashes. |
| **Authentication** | Django’s stock login/logout + custom signup view; `LoginRequiredMixin` protects all finance views. |
| **Unit Tests** | `finance/tests.py` covers model validation & basic calculations. |

---

## 🛠️ Tech Stack

- **Python 3.13** (works on 3.10 +)
- **Django 5.x**
- sqlite (default) for dev storage
- pytest / unittest built‑ins
- Optional: `python-dotenv` or `django-environ` for `.env`

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

# 4 ⃣ Environment vars
cp .env.example .env                 # or create .env manually
# Edit .env and set:
#   SECRET_KEY=django-insecure-<random-string>
#   DEBUG=True

# 5 ⃣ DB setup
python manage.py migrate
python manage.py createsuperuser     # follow prompts

# 6 ⃣ Run!
python manage.py runserver
# Browse http://127.0.0.1:8000/
