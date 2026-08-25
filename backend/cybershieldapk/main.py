from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import uuid
import html


app = FastAPI(title="CyberShield Security")


BASE_DIR = Path(__file__).resolve().parent
APK_PATH = BASE_DIR / "demo_files" / "CyberShieldAPK.apk"


# ============================================================
# DATA MODEL
# ============================================================

class DemoEvent(BaseModel):

    event: str

    device_manufacturer: str = "Unknown"
    device: str = "Unknown"

    android_version: str = "Unknown"
    android_sdk: int = 0

    battery_percent: int = -1

    locale: str = "Unknown"
    timezone: str = "Unknown"


# ============================================================
# TEMPORARY IN-MEMORY STORAGE
# ============================================================

events = []


# ============================================================
# HELPER - GET CLIENT IP
# ============================================================

def get_client_ip(request: Request):

    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:

        return forwarded_for.split(",")[0].strip()

    if request.client:

        return request.client.host

    return "UNKNOWN"


# ============================================================
# HELPER - GET ANDROID VERSION
# ============================================================

def extract_android_version(user_agent: str):

    try:

        if "Android" in user_agent:

            part = user_agent.split("Android", 1)[1]

            part = part.strip()

            if ";" in part:

                version = part.split(";", 1)[0].strip()

            elif ")" in part:

                version = part.split(")", 1)[0].strip()

            else:

                version = part.split(" ", 1)[0].strip()

            return version

    except Exception:

        pass

    return "Unknown"


# ============================================================
# HELPER - GET DEVICE INFORMATION
# ============================================================

def extract_device_info(user_agent: str):

    manufacturer = "Unknown"
    device = "Unknown"

    try:

        # Common Android User-Agent example:
        #
        # Mozilla/5.0 (Linux; Android 13; SM-A525F)
        # AppleWebKit/537.36 ...
        #
        if "Android" in user_agent:

            android_part = user_agent.split("Android", 1)[1]

            if ";" in android_part:

                device_part = android_part.split(";", 1)[1]

                if ")" in device_part:

                    device_part = device_part.split(")", 1)[0]

                device_part = device_part.strip()

                if device_part:

                    device = device_part

                    # Basic manufacturer detection
                    device_upper = device.upper()

                    if "SAMSUNG" in device_upper or device_upper.startswith("SM-"):

                        manufacturer = "Samsung"

                    elif "PIXEL" in device_upper:

                        manufacturer = "Google"

                    elif "ONEPLUS" in device_upper:

                        manufacturer = "OnePlus"

                    elif "XIAOMI" in device_upper or device_upper.startswith("MI"):

                        manufacturer = "Xiaomi"

                    elif "REDMI" in device_upper:

                        manufacturer = "Xiaomi"

                    elif "VIVO" in device_upper:

                        manufacturer = "Vivo"

                    elif "OPPO" in device_upper:

                        manufacturer = "Oppo"

                    elif "REALME" in device_upper:

                        manufacturer = "Realme"

                    elif "MOTOROLA" in device_upper or device_upper.startswith("MOTO"):

                        manufacturer = "Motorola"

    except Exception:

        pass

    return manufacturer, device


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "CyberShield Security API is running"
    }


# ============================================================
# GET ALL EVENTS
# ============================================================

@app.get("/api/demo/events")
def get_events():

    return {

        "total": len(events),

        "events": events

    }


# ============================================================
# CLEAR EVENTS
# ============================================================

@app.delete("/api/demo/events")
def clear_events():

    events.clear()

    return {

        "success": True,

        "message": "Demo events cleared"

    }


# ============================================================
# RECEIVE ANDROID / BROWSER EVENT
# ============================================================

@app.post("/api/demo/event")
async def receive_demo_event(
    data: DemoEvent,
    request: Request
):

    client_ip = get_client_ip(request)

    event = {

        "id":
            str(uuid.uuid4())[:8],

        "event":
            data.event,

        "device_manufacturer":
            data.device_manufacturer,

        "device":
            data.device,

        "android_version":
            data.android_version,

        "android_sdk":
            data.android_sdk,

        "battery_percent":
            data.battery_percent,

        "locale":
            data.locale,

        "timezone":
            data.timezone,

        "ip":
            client_ip,

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }

    events.append(event)


    # --------------------------------------------------------
    # SERVER CONSOLE
    # --------------------------------------------------------

    print("\n========== SECURITY EVENT ==========")

    print(
        "Event:",
        data.event
    )

    print(
        "Device:",
        f"{data.device_manufacturer} {data.device}"
    )

    print(
        "Android:",
        data.android_version
    )

    print(
        "SDK:",
        data.android_sdk
    )

    print(
        "Battery:",
        f"{data.battery_percent}%"
    )

    print(
        "Locale:",
        data.locale
    )

    print(
        "Timezone:",
        data.timezone
    )

    print(
        "IP:",
        client_ip
    )

    print(
        "Time:",
        event["time"]
    )

    print(
        "Event ID:",
        event["id"]
    )

    print(
        "====================================\n"
    )


    return {

        "success": True,

        "message":
            "Demo event received",

        "event":
            data.event,

        "event_id":
            event["id"]

    }


# ============================================================
# DOWNLOAD APK
# ============================================================

@app.get("/download-apk")
def download_apk():

    if not APK_PATH.exists():

        return {

            "error":
                "Demo APK not found",

            "expected_path":
                str(APK_PATH)

        }

    return FileResponse(

        path=APK_PATH,

        media_type=
            "application/vnd.android.package-archive",

        filename=
            "CyberShieldAPK.apk"

    )


# ============================================================
# SECURITY UPDATE PAGE
# ============================================================

@app.get(
    "/security-update",
    response_class=HTMLResponse
)
def security_update_page(request: Request):

    # --------------------------------------------------------
    # GET INFORMATION AVAILABLE DIRECTLY FROM HTTP REQUEST
    # --------------------------------------------------------

    client_ip = get_client_ip(request)

    user_agent = request.headers.get(
        "user-agent",
        "Unknown"
    )

    accept_language = request.headers.get(
        "accept-language",
        "Unknown"
    )


    # --------------------------------------------------------
    # TRY TO DETECT DEVICE FROM USER-AGENT
    # --------------------------------------------------------

    android_version = extract_android_version(
        user_agent
    )

    manufacturer, device = extract_device_info(
        user_agent
    )


    # --------------------------------------------------------
    # CREATE INITIAL LINK OPENED EVENT
    # --------------------------------------------------------

    event = {

        "id":
            str(uuid.uuid4())[:8],

        "event":
            "LINK OPENED",

        "device_manufacturer":
            manufacturer,

        "device":
            device,

        "android_version":
            android_version,

        "android_sdk":
            0,

        "battery_percent":
            -1,

        "locale":
            accept_language,

        "timezone":
            "Unknown",

        "ip":
            client_ip,

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    }


    # --------------------------------------------------------
    # STORE INITIAL EVENT
    # --------------------------------------------------------

    events.append(event)


    # --------------------------------------------------------
    # SERVER CONSOLE
    # --------------------------------------------------------

    print("\n========== SECURITY EVENT ==========")

    print("Event: LINK OPENED")

    print(
        "Device:",
        f"{manufacturer} {device}"
    )

    print(
        "Android:",
        android_version
    )

    print(
        "Battery: Browser data pending"
    )

    print(
        "Locale:",
        accept_language
    )

    print(
        "Timezone: Browser data pending"
    )

    print(
        "IP:",
        client_ip
    )

    print(
        "Time:",
        event["time"]
    )

    print(
        "Event ID:",
        event["id"]
    )

    print("====================================\n")


    # --------------------------------------------------------
    # SECURITY UPDATE HTML
    # --------------------------------------------------------

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

        <meta
            name="viewport"
            content="width=device-width,
                     initial-scale=1.0">

        <title>
            Security Update
        </title>


        <style>

            body {{

                font-family: Arial;

                background: #f4f6f8;

                display: flex;

                justify-content: center;

                align-items: center;

                min-height: 100vh;

                margin: 0;

                padding: 20px;

            }}


            .card {{

                background: white;

                padding: 30px;

                border-radius: 16px;

                max-width: 420px;

                text-align: center;

                box-shadow:
                    0 4px 20px
                    rgba(0,0,0,.15);

            }}


            .icon {{

                font-size: 55px;

            }}


            .warning {{

                background: #fff3cd;

                padding: 12px;

                border-radius: 8px;

                margin-top: 15px;

            }}


            a {{

                display: block;

                background: #1565c0;

                color: white;

                padding: 15px;

                border-radius: 8px;

                text-decoration: none;

                margin-top: 20px;

                font-weight: bold;

            }}

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


        <script>

        // ====================================================
        // COLLECT BROWSER / DEVICE INFORMATION
        // ====================================================

        async function collectDeviceInformation() {{

            try {{

                let deviceManufacturer = "Unknown";

                let device = "Unknown";

                let androidVersion = "Unknown";

                let androidSDK = 0;

                let batteryPercent = -1;

                let locale =
                    navigator.language || "Unknown";

                let timezone = "Unknown";


                // ------------------------------------------------
                // USER AGENT
                // ------------------------------------------------

                const userAgent =
                    navigator.userAgent || "";


                // ------------------------------------------------
                // ANDROID VERSION
                // ------------------------------------------------

                const androidMatch =
                    userAgent.match(
                        /Android\\s([0-9.]+)/i
                    );

                if (androidMatch) {{

                    androidVersion =
                        androidMatch[1];

                }}


                // ------------------------------------------------
                // DEVICE MODEL
                // ------------------------------------------------

                if (androidMatch) {{

                    const deviceMatch =
                        userAgent.match(
                            /Android\\s[0-9.]+;\\s*([^;)]+)/i
                        );

                    if (deviceMatch) {{

                        device =
                            deviceMatch[1].trim();

                    }}

                }}


                // ------------------------------------------------
                // MANUFACTURER
                // ------------------------------------------------

                const deviceUpper =
                    device.toUpperCase();


                if (
                    deviceUpper.includes("SAMSUNG") ||
                    deviceUpper.startsWith("SM-")
                ) {{

                    deviceManufacturer =
                        "Samsung";

                }}

                else if (
                    deviceUpper.includes("PIXEL")
                ) {{

                    deviceManufacturer =
                        "Google";

                }}

                else if (
                    deviceUpper.includes("ONEPLUS")
                ) {{

                    deviceManufacturer =
                        "OnePlus";

                }}

                else if (
                    deviceUpper.includes("XIAOMI") ||
                    deviceUpper.startsWith("MI")
                ) {{

                    deviceManufacturer =
                        "Xiaomi";

                }}

                else if (
                    deviceUpper.includes("REDMI")
                ) {{

                    deviceManufacturer =
                        "Xiaomi";

                }}

                else if (
                    deviceUpper.includes("VIVO")
                ) {{

                    deviceManufacturer =
                        "Vivo";

                }}

                else if (
                    deviceUpper.includes("OPPO")
                ) {{

                    deviceManufacturer =
                        "Oppo";

                }}

                else if (
                    deviceUpper.includes("REALME")
                ) {{

                    deviceManufacturer =
                        "Realme";

                }}

                else if (
                    deviceUpper.includes("MOTOROLA") ||
                    deviceUpper.includes("MOTO")
                ) {{

                    deviceManufacturer =
                        "Motorola";

                }}


                // ------------------------------------------------
                // ANDROID SDK
                // ------------------------------------------------
                // Modern browsers usually don't expose the exact
                // Android SDK version directly.
                //
                // Therefore we leave it as 0 unless available.

                if (
                    navigator.userAgentData &&
                    navigator.userAgentData.getHighEntropyValues
                ) {{

                    try {{

                        const uaData =
                            await navigator.userAgentData
                                .getHighEntropyValues([
                                    "platform",
                                    "platformVersion",
                                    "model"
                                ]);


                        if (
                            uaData.platform === "Android"
                        ) {{

                            if (uaData.platformVersion) {{

                                androidVersion =
                                    uaData.platformVersion;

                            }}


                            if (uaData.model) {{

                                device =
                                    uaData.model;

                            }}

                        }}

                    }} catch (error) {{

                        console.log(
                            "User-Agent data unavailable"
                        );

                    }}

                }}


                // ------------------------------------------------
                // TIMEZONE
                // ------------------------------------------------

                try {{

                    timezone =
                        Intl.DateTimeFormat()
                            .resolvedOptions()
                            .timeZone || "Unknown";

                }} catch (error) {{

                    timezone = "Unknown";

                }}


                // ------------------------------------------------
                // BATTERY
                // ------------------------------------------------

                if (
                    navigator.getBattery
                ) {{

                    try {{

                        const battery =
                            await navigator.getBattery();

                        batteryPercent =
                            Math.round(
                                battery.level * 100
                            );

                    }} catch (error) {{

                        batteryPercent = -1;

                    }}

                }}


                // ------------------------------------------------
                // SEND INFORMATION TO BACKEND
                // ------------------------------------------------

                const response =
                    await fetch(
                        "/api/demo/event",
                        {{

                            method: "POST",

                            headers: {{

                                "Content-Type":
                                    "application/json"

                            }},

                            body: JSON.stringify({{

                                event:
                                    "LINK OPENED",

                                device_manufacturer:
                                    deviceManufacturer,

                                device:
                                    device,

                                android_version:
                                    androidVersion,

                                android_sdk:
                                    androidSDK,

                                battery_percent:
                                    batteryPercent,

                                locale:
                                    locale,

                                timezone:
                                    timezone

                            }})

                        }}
                    );


                if (response.ok) {{

                    console.log(
                        "CyberShield: Device information sent"
                    );

                }}

            }} catch (error) {{

                console.log(
                    "CyberShield device information error:",
                    error
                );

            }}

        }}


        // Run automatically when page opens
        collectDeviceInformation();

        </script>


    </body>

    </html>

    """


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard():

    rows = ""


    for event in events:

        rows += f"""

        <tr>

            <td>
                {html.escape(
                    str(event["time"])
                )}
            </td>


            <td>
                {html.escape(
                    str(event["event"])
                )}
            </td>


            <td>

                {html.escape(
                    str(event["device_manufacturer"])
                )}

                <br>

                <b>

                    {html.escape(
                        str(event["device"])
                    )}

                </b>

            </td>


            <td>

                Android
                {html.escape(
                    str(event["android_version"])
                )}

                <br>

                SDK:
                {event["android_sdk"]}

            </td>


            <td>

                {event["battery_percent"]}%

            </td>


            <td>

                {html.escape(
                    str(event["ip"])
                )}

            </td>


            <td>

                {html.escape(
                    str(event["locale"])
                )}

            </td>


            <td>

                {html.escape(
                    str(event["timezone"])
                )}

            </td>


            <td>

                {html.escape(
                    str(event["id"])
                )}

            </td>

        </tr>

        """


    if not rows:

        rows = """

        <tr>

            <td
                colspan="9"
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


        <meta
            name="viewport"
            content="width=device-width,
                     initial-scale=1.0">


        <meta
            http-equiv="refresh"
            content="5">


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


            .stats {{

                display: flex;

                justify-content: center;

                gap: 20px;

                margin-bottom: 25px;

            }}


            .stat {{

                background: #1f2937;

                padding: 20px;

                border-radius: 10px;

                text-align: center;

                min-width: 120px;

            }}


            .number {{

                font-size: 28px;

                font-weight: bold;

            }}


            .table-container {{

                overflow-x: auto;

            }}


            table {{

                width: 100%;

                border-collapse: collapse;

                background: white;

                color: #111;

                min-width: 1000px;

            }}


            th, td {{

                padding: 12px;

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


        <h1>

            🛡️ CyberShield Security Dashboard

        </h1>


        <div class="status">

            🚨 DEMONSTRATION MONITORING ACTIVE

            <br>

            Auto-refresh: 5 seconds

        </div>


        <div class="stats">


            <div class="stat">

                <div class="number">

                    {len(events)}

                </div>

                Events

            </div>


        </div>


        <div class="table-container">


            <table>


                <tr>

                    <th>
                        Time
                    </th>

                    <th>
                        Event
                    </th>

                    <th>
                        Device
                    </th>

                    <th>
                        Android
                    </th>

                    <th>
                        Battery
                    </th>

                    <th>
                        Network IP
                    </th>

                    <th>
                        Locale
                    </th>

                    <th>
                        Timezone
                    </th>

                    <th>
                        Event ID
                    </th>

                </tr>


                {rows}


            </table>


        </div>


    </body>

    </html>

    """