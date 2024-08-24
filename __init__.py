from flask import Flask

app = Flask(__name__)

# Default to DevelopmentConfig if no ENV is set
env = app.config.get("ENV", "development")

if env == "production":
    app.config.from_object("config.ProductionConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views
