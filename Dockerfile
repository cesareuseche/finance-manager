# 1) Start from a Python base
FROM python:3.10-slim

# 2) Install Node.js (for Sass) and build essentials
RUN apt-get update \
  && apt-get install -y curl build-essential \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# 3) Set workdir & copy requirements
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# 4) Copy project files
COPY . .

# 5) Install your npm deps (sass CLI, etc.)
RUN npm install

# 6) Make the entrypoint script executable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 7) Expose Django’s default port
EXPOSE 8000

# 8) Use the script to launch both processes
ENTRYPOINT ["entrypoint.sh"]
