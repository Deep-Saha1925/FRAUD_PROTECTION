from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="CyberShield Security Demo")


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