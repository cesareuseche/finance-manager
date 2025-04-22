# 💰 Personal Finance Manager (Django 5)

A minimalist, self‑hosted web app to track income and expenses, view running totals, and export your data. Built for the PRG 402 syllabus, tested on macOS (Apple Silicon) & Linux.

---

## ✨ Core Features

- **Add & Manage Entries**: Enter income (source + amount) and expenses (description, category, amount, date). Create and delete entries as needed.
- **Per‑User Dashboard**: Each authenticated user sees only their own data, with totals for income, expenses, and balance.
- **File Persistence**: Creates JSON (`data/finance_data.json`) and CSV‑style text (`data/finance_data.txt`) on every change via Django signals.
- **Validation & Errors**: Server‑side checks for positive amounts, required fields per entry type, and date not in the future. Clear error messages.
- **Authentication**: Django’s built‑in auth with a custom signup view; all finance views use `LoginRequiredMixin`.
- **Unit Tests**: `finance/tests.py` covers model validation and calculations.

---

## 🛠️ Tech Stack

- **Python 3.13** (compatible with 3.10+)
- **Django 5.2**
- **SQLite** (default) or **PostgreSQL**
- **python-dotenv** for environment variable management
- **SCSS/Sass** for styling (via npm)

---

## 🚀 Local Development (Without Docker)

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your‑user>/finance-manager.git
   cd finance-manager
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # .\.venv\Scripts\Activate.ps1 on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env:
   SECRET_KEY=django-insecure-<your-secret>
   DEBUG=True
   ```

5. **Run database migrations & superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Build assets & start server**
   ```bash
   npm run build:css
   python manage.py runserver
   ```

Point your browser to http://127.0.0.1:8000/.

---

## 🐳 Docker & Docker Compose

You can run the entire stack in containers—no local Python or Node installs required.

### 1. Build the images

```bash
docker-compose build
```

### 2. Start services

```bash
docker-compose up -d
```

This will start:
- **web** (Django + Gunicorn + static build)
- **db** (PostgreSQL)

### 3. Run migrations & create a superuser

```bash
docker-compose exec web python manage.py migrate
```

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. View logs (optional)

```bash
docker-compose logs -f web
```

### 5. Run the test suite

```bash
docker-compose exec web python manage.py test
```

### 6. Shutdown & cleanup

```bash
docker-compose down
```

To remove volumes (data) as well:

```bash
docker-compose down -v
```

---

## ✅ Testing

Locally (outside Docker):

```bash
python manage.py test
```

In Docker:

```bash
docker-compose exec web python manage.py test
```

---

## 📄 License

MIT © Cesar Useche

