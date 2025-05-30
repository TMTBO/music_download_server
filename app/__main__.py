from . import app

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=app.config.get("PORT", 5050),
        debug=app.config.get("DEBUG", True)
    )