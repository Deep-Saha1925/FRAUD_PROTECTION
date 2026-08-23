from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="CyberShield Security Demo")

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)
APK_PATH = BASE_DIR / "demo_files" / "CyberShieldAPK.apk"

class DemoEvent(BaseModel):
    demo_id: str
    platform: str
    app_version: str
    event: str


@app.get("/")
def root():
    return {
        "message": "CyberShield Security Demo API is running"
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