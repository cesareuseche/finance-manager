# 💰 Personal Finance Manager (Django 5)

A minimalist, self‑hosted web app to track income and expenses, view running totals, and export your data. Built for the PRG 402 syllabus, tested on macOS (Apple Silicon) & Linux.

---

## ✨ Core Features

| Feature                 | Details                                                                                             |
|-------------------------|-----------------------------------------------------------------------------------------------------|
| **Add & Manage Entries**| Enter income (source + amount) and expenses (description, category, amount, date). Create and delete entries as needed. |
| **Per‑User Dashboard**  | Each authenticated user sees only their own data, with totals for income, expenses, and balance.    |
| **File Persistence**    | Creates JSON (`data/finance_data.json`) and CSV‑style text (`data/finance_data.txt`) on every change via Django signals. |
| **Validation & Errors** | Server‑side checks: positive amounts, required fields per entry type, date not in the future. Clear error messages. |
| **Authentication**      | Django’s built‑in auth with a custom signup view. All finance views use `LoginRequiredMixin`.       |
| **Unit Tests**          | `finance/tests.py` covers model validation and calculations.                                       |

---

## 🛠️ Tech Stack

- **Python 3.13** (compatible with 3.10+)
- **Django 5.2**
- **SQLite** (default) for storage
- **python-dotenv** for environment variable management
- **SCSS/Sass** for styling (via npm)

---

## 🚀 Local Development

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your‑user>/finance-manager.git
   cd finance-manager
   ```

2. **Create & activate a virtual environment**
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   - Copy `.env.example` to `.env` and set:
     ```dotenv
     SECRET_KEY=django-insecure-<your-random-secret>
     DEBUG=True
     ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Build CSS (optional)**
   ```bash
   npm install
   npm run build:css
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

Browse the app at <http://127.0.0.1:8000/>.

---

## 🐳 Docker & Docker Compose

### Dockerfile (example)

```dockerfile
# 1. Build stage
FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Final stage
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .

# Environment
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Expose port
EXPOSE 8000

# Collect static files
RUN apt-get update && apt-get install -y nodejs npm && \
    npm install && npm run build:css && rm -rf /var/lib/apt/lists/*

# Entry point
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml (example)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - data:/app/data
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: "postgres:15"
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=finance
n      - POSTGRES_PASSWORD=finance
      - POSTGRES_DB=finance_db

volumes:
  data:
  pgdata:
```

1. **Build & run**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations & create superuser**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

3. **Access**
   <http://127.0.0.1:8000/>

---

## ✅ Testing

```bash
python manage.py test
```

---

## 📄 License

MIT © <Cesar Useche>