# WSGI entry point for production servers (gunicorn, uWSGI, etc.)
# The server should point to `wsgi:application`
from app import app

# Provide `application` symbol commonly expected by WSGI servers
application = app

if __name__ == "__main__":
    # Allow running the app directly for quick manual tests
    app.run(host="0.0.0.0", port=5000)
