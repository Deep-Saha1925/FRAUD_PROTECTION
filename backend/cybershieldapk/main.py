from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import uuid

app = FastAPI(title="CyberShield Security")

BASE_DIR = Path(__file__).resolve().parent
APK_PATH = BASE_DIR / "demo_files" / "CyberShieldAPK.apk"


# =========================
# DATA MODEL
# =========================

class DemoEvent(BaseModel):
    demo_id: str
    platform: str
    app_version: str
    event: str
    device: str = "Unknown"


# Temporary storage for demonstration
events = []


# =========================
# HELPER
# =========================

def get_client_ip(request: Request):

    # Render/reverse proxy may forward the original client IP
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "UNKNOWN"


# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "message": "CyberShield Security API is running"
    }

@app.get("/api/demo/events")
def get_events():

    return {
        "total": len(events),
        "events": events
    }

@app.delete("/api/demo/events")
def clear_events():

    events.clear()

    return {
        "success": True,
        "message": "Demo events cleared"
    }

# =========================
# RECEIVE ANDROID EVENT
# =========================

@app.post("/api/demo/event")
async def receive_demo_event(
    data: DemoEvent,
    request: Request
):

    client_ip = get_client_ip(request)

    event = {
        "id": str(uuid.uuid4())[:8],
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
    print("App Version:", data.app_version)
    print("IP:", client_ip)
    print("Time:", event["time"])
    print("====================================\n")

    return {
        "success": True,
        "message": "Demo event received",
        "event": data.event,
        "demo_id": data.demo_id
    }


# =========================
# DOWNLOAD APK
# =========================

@app.get("/download-apk")
def download_apk():

    if not APK_PATH.exists():

        return {
            "error": "Demo APK not found",
            "expected_path": str(APK_PATH)
        }

    return FileResponse(
        path=APK_PATH,
        media_type="application/vnd.android.package-archive",
        filename="CyberShieldAPK.apk"
    )


# =========================
# SECURITY UPDATE PAGE
# =========================

@app.get("/security-update", response_class=HTMLResponse)
def security_update_page():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Security Update</title>

        <style>

            body {
                font-family: Arial;
                background: #f4f6f8;

                display: flex;
                justify-content: center;
                align-items: center;

                min-height: 100vh;

                margin: 0;
                padding: 20px;
            }

            .card {

                background: white;

                padding: 30px;

                border-radius: 16px;

                max-width: 420px;

                text-align: center;

                box-shadow:
                    0 4px 20px rgba(0,0,0,.15);
            }

            .icon {

                font-size: 55px;

            }

            .warning {

                background: #fff3cd;

                padding: 12px;

                border-radius: 8px;

                margin-top: 15px;
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


            <div class="icon">

                🔒

            </div>


            <h1>

                Security Update Required

            </h1>


            <p>

                A security update is available
                for your Android device.

            </p>


            <div class="warning">

                ⚠️ CYBERSHIELD SECURITY
                DEMONSTRATION

            </div>


            <a href="/download-apk">

                Download Security Update

            </a>


        </div>


    </body>

    </html>
    """


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    rows = ""

    for event in events:

        rows += f"""
        <tr>

            <td>{event["time"]}</td>

            <td>{event["app_version"]}</td>

            <td>{event["ip"]}</td>

            <td>{event["event"]}</td>

            <td>{event["platform"]}</td>

            <td>{event["demo_id"]}</td>

        </tr>
        """


    if not rows:

        rows = """
        <tr>

            <td colspan="6"
                style="text-align:center">

                No events received yet.

            </td>

        </tr>
        """


    return f"""

    <!DOCTYPE html>

    <html>

    <head>

        <title>
            CyberShield Dashboard
        </title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">


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


            .table-container {{

                overflow-x: auto;

            }}


            table {{

                width: 100%;

                border-collapse: collapse;

                background: white;

                color: #111;

            }}


            th, td {{

                padding: 14px;

                border: 1px solid #ddd;

                text-align: left;

                white-space: nowrap;

            }}


            th {{

                background: #1565c0;

                color: white;

            }}

        </style>

    </head>


    <body>


        <h1>

            🛡️ CyberShield Security Dashboard

        </h1>


        <div class="status">

            🚨 DEMONSTRATION MONITORING ACTIVE

        </div>


        <div class="table-container">

            <table>

                <tr>

                    <th>Time</th>

                    <th>App Version</th>

                    <th>DEVICE IP</th>

                    <th>Event</th>

                    <th>Platform</th>

                    <th>Demo ID</th>

                </tr>

                {rows}

            </table>

        </div>


    </body>

    </html>

    """