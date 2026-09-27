import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Local development only. Binds to loopback and keeps the debugger off,
    # because the Werkzeug debugger allows arbitrary code execution.
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
