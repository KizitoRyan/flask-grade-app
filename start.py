import os
import subprocess

port = os.environ.get("PORT", "8000")
print(f"Starting gunicorn on port {port}", flush=True)
subprocess.run(["gunicorn", "app:app", "--bind", f"0.0.0.0:{port}", "--workers", "2", "--log-level", "debug"])
