
# Data Analyst Portfolio (Flask + HTML/CSS/JS)

A modern, 2025-ready portfolio for data analysts with separate pages for Home, About, Projects, Achievements, and Contact.

## Features
- Flask backend with SQLite to store contact messages
- TailwindCSS (CDN) + custom styles for a sleek, modern UI
- Projects & achievements populated from JSON (`/data`)
- Search & tech filter on Projects page
- SEO basics: sitemap.xml, robots.txt
- Simple admin JSON endpoint to view messages (use `?token=let-me-in` or set `ADMIN_TOKEN` env)
- Ready to deploy anywhere (Render, Railway, Fly.io, etc.)

## Quick Start

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit: http://127.0.0.1:5000

## Customize Content
Edit files in `/data`:
- `profile.json` for your bio, socials, and skills
- `projects.json` for portfolio projects
- `achievements.json` for achievements/timeline

Put your `resume.pdf` inside `/static/` to enable the resume download link.

## Environment Variables (optional)
- `SECRET_KEY` for session security
- `DATABASE_URL` to use Postgres/other database in production
- `ADMIN_TOKEN` for `/messages.json`

## Deploy
- Create a production server entry (e.g., `gunicorn 'app:create_app()'`).
- Set environment variables and `DATABASE_URL` in your platform.
- Map root path to the web service, ensure instance folder is writable.

## License
MIT — do whatever you want, just keep the credit.
