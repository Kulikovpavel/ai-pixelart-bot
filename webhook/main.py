import requests
import os


project = os.environ["PROJECT"]


def webhook(request):
    if request.method == "POST":
        url = f"https://us-central1-{project}.cloudfunctions.net/convert"
        try:
            r = requests.post(url, json=request.get_json(force=True), timeout=1)
        except requests.exceptions.Timeout:
            pass
        except Exception:
            raise
    return "ok"
