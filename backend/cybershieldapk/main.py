from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

app = FastAPI(title="CyberShield Security")

BASE_DIR = Path(__file__).resolve().parent
APK_PATH = BASE_DIR / "demo_files" / "CyberShieldAPK.apk"

class DemoEvent(BaseModel):
    demo_id: str
    platform: str
    app_version: str
    event: str

events = []

@app.get("/")
def root():
    return {
        "message": "CyberShield Security API is running"
    }


@app.post("/api/demo/event")
def receive_demo_event(data: DemoEvent):

    event = {
        "demo_id": data.demo_id,
        "platform": data.platform,
        "app_version": data.app_version,
        "event": data.event,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    events.append(event)

    print("\n========== SECURITY EVENT ==========")
    print(event)
    print("====================================\n")

    return {
        "success": True,
        "message": "Demo event received"
    }

@app.get("/download-apk")
def download_apk():
    if not APK_PATH.exists():
        return {
            "error": "Demo APK not found",
            "expected_path": str(APK_PATH)
        }

    return FileResponse(
        path=APK_PATH,
        media_type="application/vnd.android.package-archieve",
        filename="CyberShieldAPK.apk"
    )

@app.get("/security-update", response_class=HTMLResponse)
def security_update_page():

    events.append({
        "demo_id": "DEMO-001",
        "platform": "Android",
        "app_version": "WEB",
        "event": "LINK_OPENED",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Security Update</title>

        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 16px;
                max-width: 420px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,.15);
            }

            .icon {
                font-size: 55px;
            }

            .warning {
                background: #fff3cd;
                padding: 12px;
                border-radius: 8px;
            }

            a {
                display: block;
                background: #1565c0;
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
            }
        </style>
    </head>

    <body>

        <div class="card">

            <div class="icon">🔒</div>

            <h1>Security Update Required</h1>

            <p>
                A security update is available for your Android device.
            </p>

            <div class="warning">
                ⚠️ CYBERSHIELD SECURITY DEMONSTRATION
            </div>

            <a href="/download-apk">
                Download Security Update
            </a>

        </div>

    </body>
    </html>
    """
