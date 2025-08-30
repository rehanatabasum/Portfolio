import os
import json
import logging
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_from_directory, jsonify
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, send_from_directory, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("WVLAxgQmHa7ONSGMojhjH_gQZtYP4yYa5aLxe90uO6s", "change-this-secret")
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("portfolio")

    def load_json(filename):
        try:
            p = os.path.join(app.root_path, "data", filename)
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return {}

    @app.context_processor
    def inject_now():
        return {"year_now": datetime.utcnow().year}

    @app.after_request
    def add_headers(resp):
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        resp.headers["Cache-Control"] = "public, max-age=3600"
        return resp

    @app.route("/")
    def home():
        profile = load_json("profile.json")
        projects = load_json("projects.json")[:6]
        return render_template("index.html", profile=profile, projects=projects)

    @app.route("/about")
    def about():
        profile = load_json("profile.json")
        return render_template("about.html", profile=profile)

    @app.route("/projects")
    def projects():
        profile = load_json("profile.json")
        projects = load_json("projects.json")
        return render_template("projects.html", profile=profile, projects=projects)

    @app.route("/achievements")
    def achievements():
        profile = load_json("profile.json")
        achievements = load_json("achievements.json")
        return render_template("achievements.html", profile=profile, achievements=achievements)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        profile = load_json("profile.json")
        if request.method == "POST":
            if request.form.get("website"):  
                flash("Thanks!", "success")
                return redirect(url_for("contact"))

            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not message:
                flash("Please fill in your name, email and message.", "error")
                return redirect(url_for("contact"))

            flash("Your message has been received. Thank you!", "success")
            logger.info(f"New message from {name} <{email}>")
            return redirect(url_for("contact"))

        return render_template("contact.html", profile=profile)

    @app.route("/api/messages")
    def messages_json():
        return jsonify({"error": "DB disabled, messages unavailable"}), 403

    @app.route("/sitemap.xml")
    def sitemap():
        urls = [url_for("home", _external=True)]
        urls += [url_for(p, _external=True) for p in ["about", "projects", "achievements", "contact"]]
        xml = ["<?xml version='1.0' encoding='UTF-8'?>",
               "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
        for u in urls:
            xml.append(f"<url><loc>{u}</loc></url>")
        xml.append("</urlset>")
        return app.response_class("\n".join(xml), mimetype="application/xml")

    @app.route("/robots.txt")
    def robots():
        return app.response_class(
            f"User-agent: *\nAllow: /\nSitemap: {url_for('sitemap', _external=True)}",
            mimetype="text/plain"
        )


    @app.errorhandler(404)
    def not_found(e):
     profile = load_json("profile.json")
     return render_template(
        "base.html", profile=profile,
        content_title="Not Found",
        content_sub="The page you requested was not found."
    ), 404

    @app.errorhandler(500)
    def server_error(e):
        profile = load_json("profile.json")
        return render_template(
            "base.html", profile=profile,
            content_title="Server Error",
            content_sub="Oops! Something went wrong."
        ), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
