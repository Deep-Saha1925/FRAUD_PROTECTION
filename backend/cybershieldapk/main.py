from fastapi import FastAPI, Request
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
async def receive_demo_event(
    data: DemoEvent,
    request: Request
):

    client_ip = request.client.host if request.client else "UNKNOWN"

    event = {
        "demo_id": data.demo_id,
        "platform": data.platform,
        "app_version": data.app_version,
        "event": data.event,
        "ip": client_ip,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    events.append(event)

    print("\n========== SECURITY EVENT ==========")
    print("Event:", data.event)
    print("Demo ID:", data.demo_id)
    print("Platform:", data.platform)
    print("IP:", client_ip)
    print("Time:", event["time"])
    print("====================================\n")

    return {
        "success": True,
        "message": "Demo event received",
        "event": data.event
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

    print(events)

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

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    rows = ""

    for event in events:
        rows += f"""
        <tr>
            <td>{event["time"]}</td>
            <td>{event["event"]}</td>
            <td>{event["platform"]}</td>
            <td>{event["demo_id"]}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CyberShield Dashboard</title>

        <style>
            body {{
                font-family: Arial;
                background: #101820;
                color: white;
                padding: 30px;
            }}

            h1 {{
                text-align: center;
            }}

            .status {{
                text-align: center;
                padding: 15px;
                margin: 20px;
                background: #1f2937;
                border-radius: 10px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: #ffffff;
                color: #111;
            }}

            th, td {{
                padding: 14px;
                border: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #1565c0;
                color: white;
            }}
        </style>
    </head>

    <body>

        <h1>🛡️ CyberShield Security Dashboard</h1>

        <div class="status">
            🚨 DEMONSTRATION MONITORING ACTIVE
        </div>

        <table>
            <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Platform</th>
                <th>Demo ID</th>
            </tr>

            {rows}

        </table>

    </body>
    </html>
    """