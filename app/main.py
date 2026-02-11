from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# AUTH
from app.auth.login_api import router as login_router
from app.auth.register_api import router as register_router
from app.auth.forgot_password_api import router as forgot_password_router
from app.auth.reset_password_api import router as reset_password_router
from app.auth.otp_api import router as otp_router

# USERS
from app.users.get_profile_api import router as get_profile_router
from app.users.update_profile_api import router as update_profile_router
from app.users.change_password_api import router as change_password_router
from app.users.delete_account_api import router as delete_account_router

# ACTIVITY
from app.activity.add_activity_log_api import router as add_activity_router
from app.activity.get_activity_logs_api import router as get_activity_router

# DEVICES
from app.devices.register_device_api import router as register_device_router
from app.devices.list_devices_api import router as list_devices_router
from app.devices.delete_device_api import router as delete_device_router

# PERMISSIONS
from app.permissions.get_permissions_api import router as get_permissions_router
from app.permissions.update_permissions_api import router as update_permissions_router

# SETTINGS
from app.settings.get_settings_api import router as get_settings_router
from app.settings.update_settings_api import router as update_settings_router

# IMAGES
from app.images.upload_image_api import router as upload_image_router
from app.images.capture_image_api import router as capture_image_router
from app.images.get_images_api import router as get_images_router

# GCODE
from app.gcode.convert_image_to_gcode_api import router as convert_gcode_router
from app.gcode.process_gcode_api import router as process_gcode_router
from app.gcode.save_gcode_api import router as save_gcode_router
from app.gcode.list_gcodes_api import router as list_gcodes_router
from app.gcode.get_gcode_api import router as get_gcode_router

# DATA TRANSFER
from app.data_transfer.start_transfer_api import router as start_transfer_router
from app.data_transfer.update_transfer_progress_api import router as update_transfer_router
from app.data_transfer.transfer_history_api import router as transfer_history_router


# ---------- APP ----------
app = FastAPI(
    title="GCODE API",
    version="1.0.0"
)
from fastapi import FastAPI
from db import get_connection

app = FastAPI()

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    conn.close()
    return result

# ---------- STATIC FILES (uploads) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIR),
    name="uploads"
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- REGISTER ROUTERS ----------

# Auth
app.include_router(login_router, prefix="/auth")
app.include_router(register_router, prefix="/auth")
app.include_router(forgot_password_router, prefix="/auth")
app.include_router(reset_password_router, prefix="/auth")
app.include_router(otp_router, prefix="/auth")

# Users
app.include_router(get_profile_router, prefix="/users")
app.include_router(update_profile_router, prefix="/users")
app.include_router(change_password_router, prefix="/users")
app.include_router(delete_account_router, prefix="/users")

# Activity
app.include_router(add_activity_router, prefix="/activity")
app.include_router(get_activity_router, prefix="/activity")

# Devices
app.include_router(register_device_router, prefix="/devices")
app.include_router(list_devices_router, prefix="/devices")
app.include_router(delete_device_router, prefix="/devices")

# Permissions
app.include_router(get_permissions_router, prefix="/permissions")
app.include_router(update_permissions_router, prefix="/permissions")

# Settings
app.include_router(get_settings_router, prefix="/settings")
app.include_router(update_settings_router, prefix="/settings")

# Images
app.include_router(upload_image_router, prefix="/images")
app.include_router(capture_image_router, prefix="/images")
app.include_router(get_images_router, prefix="/images")

# GCode
app.include_router(convert_gcode_router, prefix="/gcode")
app.include_router(process_gcode_router, prefix="/gcode")
app.include_router(save_gcode_router, prefix="/gcode")
app.include_router(list_gcodes_router, prefix="/gcode")
app.include_router(get_gcode_router, prefix="/gcode")

# Data Transfer
app.include_router(start_transfer_router, prefix="/transfer")
app.include_router(update_transfer_router, prefix="/transfer")
app.include_router(transfer_history_router, prefix="/transfer")


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "GCODE API"
    }
