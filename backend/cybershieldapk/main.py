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

    print("\n========== DEMO EVENT ==========")
    print("Demo ID:", data.demo_id)
    print("Platform:", data.platform)
    print("App Version:", data.app_version)
    print("Event:", data.event)
    print("Received:", datetime.now())
    print("================================\n")

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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Security Update</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }

            .card {
                background: white;
                width: 90%;
                max-width: 420px;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,.15);
                text-align: center;
            }

            .icon {
                font-size: 55px;
            }

            h1 {
                color: #222;
            }

            p {
                color: #555;
                line-height: 1.6;
            }

            .warning {
                background: #fff3cd;
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
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

            .demo {
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }
        </style>
    </head>

    <body>

        <div class="card">

            <div class="icon">🔒</div>

            <h1>Security Update Required</h1>

            <p>
                A security update is available for your Android device.
                Install the latest security component to continue using
                protected services.
            </p>

            <div class="warning">
                ⚠️ This demonstration shows how a malicious link can
                convince a user to download an application.
            </div>

            <a href="/download-apk">
                Download Security Update
            </a>

            <div class="demo">
                CYBERSHIELD SECURITY DEMONSTRATION
            </div>

        </div>

    </body>
    </html>
    """


