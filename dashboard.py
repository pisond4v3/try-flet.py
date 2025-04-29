import flet as ft
import pygetwindow as gw
import time
import logging
from typing import List, Tuple, Dict
from datetime import datetime
from firebase_config import db
from utils import calculate_status_and_schedule, COMPONENT_DATA

# Configure logging
logging.basicConfig(filename="dashboard.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Define maintenance items with image paths
MAINTENANCE_ITEMS = [
    {"name": "Engine Oil & Oil Filter", "status": "N/A", "image": "assets/maintenance_icon/engine_oil.png",
     "color": "#fdd835"},
    {"name": "Air Filter", "status": "N/A", "image": "assets/maintenance_icon/air_filter.png", "color": "#fdd835"},
    {"name": "Tires", "status": "N/A", "image": "assets/maintenance_icon/tires.png", "color": "#fdd835"},
    {"name": "Transmission Fluid", "status": "N/A", "image": "assets/maintenance_icon/transmission_fluid.png",
     "color": "#fdd835"},
    {"name": "Fuel Filter", "status": "N/A", "image": "assets/maintenance_icon/fuel_filter.png", "color": "#fdd835"},
    {"name": "Coolant (Radiator Fluid)", "status": "N/A", "image": "assets/maintenance_icon/coolant.png",
     "color": "#fdd835"},
    {"name": "Battery", "status": "N/A", "image": "assets/maintenance_icon/battery.png", "color": "#fdd835"},
    {"name": "Brake Fluid and Pads", "status": "N/A", "image": "assets/maintenance_icon/brake_fluids-and_pads.png",
     "color": "#fdd835"},
]

def validate_date(date_str: str) -> datetime:
    """Validate and parse a date string, ensuring it is not in the future."""
    if not date_str or date_str == "N/A":
        return None
    try:
        parsed = datetime.strptime(date_str, "%m/%d/%Y")
        if parsed > datetime.now():
            logging.warning(f"Future date detected: {date_str}")
            return None
        return parsed
    except ValueError:
        logging.error(f"Invalid date format: {date_str}")
        return None

def preload_assets(page):
    start_time = time.time()
    for item in MAINTENANCE_ITEMS:
        ft.Image(src=item["image"], visible=False)
    logging.info(f"Preloaded assets in {time.time() - start_time:.2f} seconds")

def fetch_maintenance_data(user_id, vehicle_id, page):
    try:
        start_time = time.time()
        vehicle_doc = db.collection("users").document(user_id).collection("vehicles").document(vehicle_id).get()
        vehicle_data = vehicle_doc.to_dict() if vehicle_doc.exists else {
            "km_usage": 0,
            "car_age_months": 0,
            "driving_habits": {
                "acceleration_braking": "Smooth",
                "trip_length": "Long Trips",
                "road_quality": "Smooth Paved roads",
                "climate_conditions": "Dry",
                "vehicle_load": "Light",
                "fuel_quality": "High"
            }
        }
        current_km = vehicle_data.get("km_usage", 0)

        maintenance_ref = db.collection("users").document(user_id).collection("vehicles").document(
            vehicle_id).collection("maintenance").stream()
        maintenance_data = []
        for doc in maintenance_ref:
            item = next((i for i in MAINTENANCE_ITEMS if i["name"] == doc.id), None)
            if not item:
                logging.warning(f"Maintenance item {doc.id} not found in MAINTENANCE_ITEMS")
                continue
            try:
                data = doc.to_dict() if doc.exists else {
                    "status": "N/A",
                    "last_maintenance_date": "N/A",
                    "component_type": None,
                    "km_remaining": 0,
                    "prediction_reasons": [],
                    "last_maintenance_km": 0
                }
                last_maintenance_date_str = data.get("last_maintenance_date", "N/A")
                last_maintenance_date = validate_date(last_maintenance_date_str)
                if last_maintenance_date:
                    data["last_maintenance_date"] = last_maintenance_date.strftime("%m/%d/%Y")
                else:
                    data["last_maintenance_date"] = "N/A"
                    logging.warning(
                        f"Invalid or missing last_maintenance_date for {item['name']}: {last_maintenance_date_str}")

                if not data.get("component_type"):
                    component_options = COMPONENT_DATA.get(item["name"], {}).get("options", [])
                    data["component_type"] = component_options[0] if component_options else None
                    logging.info(f"Set default component_type for {item['name']}: {data['component_type']}")
                    db.collection("users").document(user_id).collection("vehicles").document(vehicle_id).collection(
                        "maintenance").document(item["name"]).set(
                        data, merge=True
                    )

                if data["last_maintenance_date"] != "N/A" and data["component_type"]:
                    try:
                        last_maintenance_km = data.get("last_maintenance_km", 0)
                        km_since_last = current_km - last_maintenance_km
                        logging.info(
                            f"Calculated km_since_last for {item['name']}: {km_since_last} (current_km={current_km}, last_maintenance_km={last_maintenance_km})")
                        adjusted_vehicle_data = vehicle_data.copy()
                        adjusted_vehicle_data["km_usage"] = km_since_last

                        status, estimated_schedule, km_remaining, reasons = calculate_status_and_schedule(
                            adjusted_vehicle_data,
                            item["name"],
                            data["last_maintenance_date"],
                            data["component_type"]
                        )
                        data["status"] = status
                        data["estimated_maintenance_schedule"] = estimated_schedule
                        data["km_remaining"] = km_remaining
                        data["prediction_reasons"] = reasons
                    except Exception as ex:
                        logging.error(f"Error calculating schedule for {item['name']}: {str(ex)}")
                        data["status"] = "N/A"
                        data["estimated_maintenance_schedule"] = "N/A"
                        data["km_remaining"] = 0
                        data["prediction_reasons"] = []
                else:
                    data["status"] = "N/A"
                    data["estimated_maintenance_schedule"] = "N/A"
                    data["km_remaining"] = 0
                    data["prediction_reasons"] = []

                db.collection("users").document(user_id).collection("vehicles").document(vehicle_id).collection(
                    "maintenance").document(item["name"]).set(
                    data, merge=True
                )
                maintenance_data.append({
                    "name": item["name"],
                    "status": data.get("status", "N/A"),
                    "last_maintenance_date": data.get("last_maintenance_date", "N/A"),
                    "estimated_maintenance_schedule": data.get("estimated_maintenance_schedule", "N/A"),
                    "component_type": data.get("component_type"),
                    "km_remaining": data.get("km_remaining", 0),
                    "prediction_reasons": data.get("prediction_reasons", []),
                    "image": item["image"],
                    "color": item["color"]
                })
            except Exception as ex:
                logging.error(f"Error processing maintenance item {item['name']}: {str(ex)}")
                continue

        for item in MAINTENANCE_ITEMS:
            if not any(m["name"] == item["name"] for m in maintenance_data):
                component_options = COMPONENT_DATA.get(item["name"], {}).get("options", [])
                component_type = component_options[0] if component_options else None
                data = {
                    "status": "N/A",
                    "last_maintenance_date": "N/A",
                    "estimated_maintenance_schedule": "N/A",
                    "component_type": component_type,
                    "km_remaining": 0,
                    "prediction_reasons": [],
                    "last_maintenance_km": 0
                }
                try:
                    db.collection("users").document(user_id).collection("vehicles").document(vehicle_id).collection(
                        "maintenance").document(item["name"]).set(
                        data, merge=True
                    )
                    maintenance_data.append({
                        "name": item["name"],
                        "status": "N/A",
                        "last_maintenance_date": "N/A",
                        "estimated_maintenance_schedule": "N/A",
                        "component_type": component_type,
                        "km_remaining": 0,
                        "prediction_reasons": [],
                        "image": item["image"],
                        "color": item["color"]
                    })
                except Exception as ex:
                    logging.error(f"Error initializing maintenance item {item['name']}: {str(ex)}")
                    continue

        validated_maintenance_data = []
        for entry in maintenance_data:
            if not isinstance(entry, dict):
                logging.error(f"Invalid maintenance data entry: {entry}")
                continue
            required_keys = ["name", "status", "last_maintenance_date", "estimated_maintenance_schedule",
                             "component_type", "km_remaining", "prediction_reasons", "image", "color"]
            if not all(key in entry for key in required_keys):
                logging.error(f"Maintenance data entry missing required keys: {entry}")
                continue
            validated_maintenance_data.append(entry)

        page.client_storage.set(f"maintenance_{vehicle_id}", validated_maintenance_data)
        logging.info(f"Fetched maintenance data for vehicle {vehicle_id} in {time.time() - start_time:.2f} seconds")
        return validated_maintenance_data
    except Exception as ex:
        logging.error(f"Error fetching maintenance data: {str(ex)}")
        return [{**item, "image": None} for item in MAINTENANCE_ITEMS]

def resize_window(title: str):
    """Resize the window to 400x800 using pygetwindow."""
    try:
        time.sleep(1)
        windows = gw.getWindowsWithTitle(title)
        if windows:
            win = windows[0]
            win.resizeTo(400, 820)
            win.moveTo(100, 100)
            logging.info(f"Resized window '{title}' to 400x820 using pygetwindow")
        else:
            logging.warning(f"Window '{title}' not found")
    except Exception as ex:
        logging.error(f"Error resizing window with pygetwindow: {str(ex)}")

def dashboard_page(page: ft.Page):
    start_page_time = time.time()
    page.title = "AUTOCARE - Dashboard"

    page.window_width = 400
    page.window_height = 820
    page.window_resizable = False

    resize_window(page.title)

    logging.info("Starting dashboard load")

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=6,
            radius=20,
            thumb_visibility=True,
            track_visibility=True,
            thumb_color="#e8e8e8",
            track_color="#656262"
        )
    )
    page.theme_mode = ft.ThemeMode.LIGHT

    preload_assets(page)

    try:
        user_id = page.client_storage.get("user_id")
        if not user_id:
            logging.warning("User not authenticated")
            print(f"Dashboard load time (unauthenticated): {time.time() - start_page_time:.2f} seconds")
            return ft.View(
                "/dashboard",
                controls=[
                    ft.Text("User not authenticated", color=ft.colors.RED, font_family="Montserrat"),
                    ft.ElevatedButton(
                        "Go to Login",
                        on_click=lambda e: page.go("/login"),
                        bgcolor="#3685cd",
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=13),
                            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                        )
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

        username = page.client_storage.get("cached_username")
        if not username or (time.time() - (page.client_storage.get("username_last_updated") or 0)) > 86400:
            try:
                start_user_time = time.time()
                user_doc = db.collection("users").document(user_id).get()
                username = user_doc.to_dict().get("username",
                                                  f"User{user_id[-3:]}") if user_doc.exists else f"User{user_id[-3:]}"
                page.client_storage.set("cached_username", username)
                page.client_storage.set("username_last_updated", time.time())
                logging.info(f"Username fetched from Firestore: {username}")
                print(f"User fetch took {time.time() - start_user_time:.2f} seconds")
            except Exception as ex:
                username = f"User{user_id[-3:]}"
                logging.error(f"Error fetching username: {str(ex)}")

        selected_car = ft.Ref[ft.Container]()
        car_components_section = ft.Ref[ft.Container]()
        delete_confirmation = ft.Ref[ft.Container]()
        vehicle_index = 0
        vehicles: List[Tuple[str, Dict]] = []
        maintenance_widgets = {}
        last_update_time = 0
        debounce_interval = 0.5

        def refresh_vehicles():
            nonlocal vehicles, vehicle_index
            try:
                vehicles_ref = db.collection("users").document(user_id).collection("vehicles").stream()
                vehicles[:] = [(doc.id, doc.to_dict()) for doc in vehicles_ref]
                vehicle_index = max(0, min(len(vehicles) - 1, vehicle_index)) if vehicles else 0
                page.client_storage.set("cached_vehicles", vehicles)
                page.client_storage.set("vehicles_last_updated", time.time())
                for vehicle_id, _ in vehicles:
                    if not page.client_storage.get(f"maintenance_{vehicle_id}"):
                        fetch_maintenance_data(user_id, vehicle_id, page)
                logging.info(f"Refreshed {len(vehicles)} vehicles from Firestore, vehicle_index={vehicle_index}")
                update_vehicle_display()
            except Exception as ex:
                logging.error(f"Error refreshing vehicles: {str(ex)}")
                page.controls.append(ft.Text(f"Error fetching vehicles: {str(ex)}", color=ft.colors.RED, size=12,
                                             font_family="Montserrat"))
                page.update()

        try:
            cached_vehicles = page.client_storage.get("cached_vehicles")
            cache_last_updated = page.client_storage.get("vehicles_last_updated") or 0
            cache_valid = cached_vehicles and (time.time() - cache_last_updated) < 86400
            if cache_valid:
                vehicles = cached_vehicles
                vehicle_index = max(0, min(len(vehicles) - 1, vehicle_index)) if vehicles else 0
                logging.info("Using cached vehicles")
                print("Vehicle fetch: Cache hit")
            else:
                refresh_vehicles()
        except Exception as ex:
            logging.error(f"Error checking vehicle cache: {str(ex)}")
            refresh_vehicles()

        def on_vehicles_snapshot(col_snapshot, changes, read_time):
            nonlocal vehicles, vehicle_index, last_update_time
            current_time = time.time()
            if current_time - last_update_time < debounce_interval:
                logging.info("Debouncing vehicles snapshot update")
                return
            last_update_time = current_time
            try:
                vehicles[:] = []
                for doc in col_snapshot:
                    try:
                        vehicle_data = doc.to_dict()
                        if not vehicle_data.get("model"):
                            logging.warning(f"Skipping invalid vehicle document {doc.id}: missing model")
                            continue
                        vehicles.append((doc.id, vehicle_data))
                    except Exception as ex:
                        logging.error(f"Error processing vehicle document {doc.id}: {str(ex)}")
                        continue
                vehicle_index = max(0, min(len(vehicles) - 1, vehicle_index)) if vehicles else 0
                page.client_storage.set("cached_vehicles", vehicles)
                page.client_storage.set("vehicles_last_updated", time.time())
                logging.info(f"Real-time update: {len(vehicles)} vehicles, vehicle_index={vehicle_index}")
                update_vehicle_display()
            except Exception as ex:
                logging.error(f"Error in vehicles snapshot: {str(ex)}")
                page.controls.append(ft.Text(f"Error updating vehicles: {str(ex)}", color=ft.colors.RED, size=12,
                                             font_family="Montserrat"))
                page.update()

        try:
            vehicles_ref = db.collection("users").document(user_id).collection("vehicles")
            snapshot_listener = vehicles_ref.on_snapshot(on_vehicles_snapshot)
            logging.info("Initialized Firestore real-time listener for vehicles")
        except Exception as ex:
            logging.error(f"Error setting up vehicles listener: {str(ex)}")
            page.controls.append(ft.Text(f"Error initializing vehicle updates: {str(ex)}", color=ft.colors.RED, size=12,
                                         font_family="Montserrat"))
            page.update()

        header_wrapper = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="assets/Dashboard header.png",
                                    width=180,
                                    height=50,
                                    fit=ft.ImageFit.CONTAIN,
                                    error_content=ft.Text("Header image not found", color=ft.colors.RED)
                                ),
                                padding=ft.padding.only(left=10, top=-5),
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Icon(
                                            name=ft.Icons.PERSON,
                                            color="#3685cd",
                                            size=20
                                        ),
                                        bgcolor="#e8e8e8",
                                        border=ft.border.all(2, "#3685cd"),
                                        padding=0,
                                        border_radius=50,
                                    ),
                                    ft.Text(
                                        username,
                                        color="#3685cd",
                                        size=14,
                                        font_family="Montserrat",
                                    ),
                                    ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=1,
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.LOGOUT,
                                                icon_color="#656262",
                                                icon_size=20,
                                                tooltip="Logout",
                                                on_click=lambda e: logout(page),
                                                padding=ft.padding.only(top=10),
                                                offset=ft.Offset(0, 0.4)
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.NOTIFICATIONS,
                                                icon_color="#656262",
                                                icon_size=20,
                                                tooltip="Notifications",
                                                offset = ft.Offset(0, 0.3)
                                            )
                                        ]
                                    ),
                                ],
                                alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=2,
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.Icons.HELP_OUTLINE, color="white", size=17),
                                            ft.Text("Need Help?", color="white", size=10),
                                        ],
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor="#3685cd",
                                        shape=ft.RoundedRectangleBorder(radius=13),
                                    ),
                                    on_click=lambda e: page.go("/customer_service")
                                ),
                                margin=ft.margin.only(left=5, top=-5),
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.Icons.NEWSPAPER, color="white", size=10),
                                            ft.Text("Automotive News", color="white", size=10),
                                        ],
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor="#3685cd",
                                        shape=ft.RoundedRectangleBorder(radius=13),
                                    ),
                                    on_click=lambda e: page.go("/automotive_news")
                                ),
                                margin=ft.margin.only(right=5, top=-5),
                            ),
                        ],
                        alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                ], spacing=-5),
                bgcolor="#e8e8e8",
                padding=ft.padding.only(top=8),
                border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
                width=370,
            ),
            bgcolor="transparent",
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
            width=370,
            height=125,
            margin=ft.margin.only(top=-23),
        )

        def update_vehicle_display():
            nonlocal vehicle_index
            delete_confirmation.current.visible = False
            logging.info(f"Updating vehicle display: vehicle_index={vehicle_index}, len(vehicles)={len(vehicles)}")
            if not vehicles:
                selected_car.current.content = ft.Container(
                    height=200,
                    alignment=ft.alignment.center,
                    padding=10,
                    content=ft.Column([
                        ft.Text(
                            "Welcome to AUTOCARE! Add your first vehicle to get started.",
                            size=18,
                            weight="bold",
                            color="#004f85",
                            font_family="Montserrat",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.DIRECTIONS_CAR, color="white", size=24),
                                    ft.Text("Add Vehicle", color="white", size=16, weight="bold",
                                            font_family="Montserrat"),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                width=150,
                                height=50,
                                bgcolor="#1ca2bf",
                                elevation=5,
                                on_click=lambda e: page.go("/add_vehicle"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE)
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                )
                car_components_section.current.visible = False
                vehicle_index = 0
                logging.info("No vehicles, showing 'Add Vehicle' UI")
            elif vehicle_index >= len(vehicles):
                selected_car.current.content = ft.Column([
                    ft.Container(
                        bgcolor="#3685cd",
                        height=50,
                        border_radius=10,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        content=ft.Row([
                            ft.Text(
                                "ADD NEW VEHICLE",
                                size=16,
                                weight="bold",
                                color="white",
                                font_family="Montserrat"
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_LEFT,
                            icon_color="#3685cd" if vehicle_index > 0 else ft.colors.GREY_500,
                            icon_size=40,
                            disabled=vehicle_index == 0,
                            on_click=lambda e: navigate_vehicle(-1),
                            tooltip="Previous Vehicle",
                            padding=ft.padding.only(left=-50),
                            offset=ft.transform.Offset(-0.5, 0)
                        ),
                        ft.Container(
                            height=150,
                            alignment=ft.alignment.center,
                            content=ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.DIRECTIONS_CAR, color="white", size=24),
                                    ft.Text("Add Vehicle", color="white", size=16, weight="bold",
                                            font_family="Montserrat"),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                width=150,
                                height=50,
                                bgcolor="#1ca2bf",
                                elevation=5,
                                on_click=lambda e: page.go("/add_vehicle"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    overlay_color=ft.colors.with_opacity(0.1, ft.colors.WHITE)
                                )
                            )
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_RIGHT,
                            icon_color=ft.colors.GREY_500,  # Always disabled on "Add Vehicle" screen
                            icon_size=40,
                            disabled=True,
                            on_click=lambda e: navigate_vehicle(1),
                            tooltip="Next Vehicle or Add Vehicle",
                            padding=ft.padding.only(left=-50),
                            offset=ft.transform.Offset(0.5, 0)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                car_components_section.current.visible = False
                logging.info("Showing 'Add Vehicle' UI")
            else:
                idx = vehicle_index % len(vehicles)
                vehicle_id, vehicle_data = vehicles[idx]
                left_arrow_disabled = vehicle_index == 0
                right_arrow_disabled = (len(vehicles) >= 3 and vehicle_index == len(vehicles) - 1) or vehicle_index == len(vehicles)
                logging.info(f"Left arrow disabled: {left_arrow_disabled}, Right arrow disabled: {right_arrow_disabled}")
                selected_car.current.content = ft.Column([
                    ft.Container(
                        bgcolor="#3685cd",
                        border_radius=10,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        content=ft.Row([
                            ft.Text(
                                vehicle_data["model"].upper(),
                                size=16,
                                weight="bold",
                                color="white",
                                font_family="Montserrat"
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color="white",
                                icon_size=20,
                                on_click=lambda e: show_delete_confirmation(vehicle_id),
                                tooltip="Delete Vehicle"
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_LEFT,
                            icon_color="#3685cd" if not left_arrow_disabled else ft.colors.GREY_500,
                            icon_size=40,
                            disabled=left_arrow_disabled,
                            on_click=lambda e: navigate_vehicle(-1),
                            tooltip="Previous Vehicle",
                            padding=ft.padding.only(left=-50),
                            offset=ft.transform.Offset(-0.5, 0)
                        ),
                        ft.Image(
                            src=f"assets/vehicles/{vehicle_data['model'].replace(' ', '_')}.png",
                            width=200,
                            height=150,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Icon(ft.Icons.DIRECTIONS_CAR, color=ft.colors.RED, size=50)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_RIGHT,
                            icon_color="#3685cd" if not right_arrow_disabled else ft.colors.GREY_500,
                            icon_size=40,
                            disabled=right_arrow_disabled,
                            on_click=lambda e: navigate_vehicle(1),
                            tooltip="Next Vehicle or Add Vehicle",
                            padding=ft.padding.only(left=-50),
                            offset=ft.transform.Offset(0.5, 0)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                car_components_section.current.visible = True
                update_maintenance_cards(vehicle_id)
            page.update()

        def navigate_vehicle(direction):
            nonlocal vehicle_index
            vehicle_index = (vehicle_index + direction) % (len(vehicles) + 1) if vehicles else 0
            vehicle_index = max(0, min(vehicle_index, len(vehicles)))
            delete_confirmation.current.visible = False
            logging.info(
                f"Navigating vehicle, direction={direction}, vehicle_index={vehicle_index}, vehicles_count={len(vehicles)}")
            update_vehicle_display()

        def update_maintenance_cards(vehicle_id):
            try:
                maintenance_data = page.client_storage.get(f"maintenance_{vehicle_id}")
                if not maintenance_data:
                    maintenance_data = fetch_maintenance_data(user_id, vehicle_id, page)
            except Exception as ex:
                logging.error(f"Error retrieving maintenance data for {vehicle_id}: {str(ex)}")
                maintenance_data = [{**item, "image": None} for item in MAINTENANCE_ITEMS]

            if vehicle_id in maintenance_widgets:
                controls = maintenance_widgets[vehicle_id]
                logging.info(f"Reusing cached maintenance widgets for vehicle {vehicle_id}")
            else:
                controls = []
                for item in maintenance_data:
                    try:
                        if not isinstance(item, dict):
                            logging.error(f"Invalid maintenance item for vehicle {vehicle_id}: {item}")
                            continue
                        required_keys = ["name", "status", "last_maintenance_date", "estimated_maintenance_schedule",
                                         "component_type", "km_remaining", "prediction_reasons", "image", "color"]
                        if not all(key in item for key in required_keys):
                            logging.error(f"Maintenance item missing required keys: {item}")
                            continue

                        container_ref = ft.Ref[ft.Container]()

                        def on_item_enter(e, cr=container_ref):
                            if cr.current:
                                cr.current.bgcolor = "#e0e0e0"
                                page.update()

                        def on_item_exit(e, cr=container_ref):
                            if cr.current:
                                cr.current.bgcolor = "#f5f5f5"
                                page.update()

                        image_path = item["image"]
                        logging.info(f"Loading image for {item['name']}: {image_path}")
                        card_content = [
                            ft.Image(
                                src=image_path,
                                width=70,
                                height=70,
                                fit=ft.ImageFit.CONTAIN,
                                error_content=ft.Icon(ft.Icons.BUILD, color="#fdd835", size=40),
                                offset=ft.Offset(.5,0)
                            ),
                            ft.Text(
                                item["name"],
                                size=12,
                                weight="bold",
                                text_align=ft.TextAlign.CENTER,
                                color="#707070",
                                font_family="Montserrat",
                            ),
                            ft.Text(
                                f"Last Maintenance: {item['last_maintenance_date']}",
                                size=10,
                                color=ft.colors.GREY,
                                font_family="Montserrat",
                                text_align=ft.TextAlign.CENTER
                            )
                        ]
                        if item["last_maintenance_date"] == "N/A":
                            card_content.append(
                                ft.Text(
                                    "Please set maintenance date",
                                    size=10,
                                    color=ft.colors.RED,
                                    font_family="Montserrat",
                                    text_align=ft.TextAlign.CENTER
                                )
                            )
                        else:
                            card_content.extend([
                                ft.Text(
                                    f"Next: {item['estimated_maintenance_schedule']}",
                                    size=10,
                                    color=ft.colors.GREY,
                                    font_family="Montserrat",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    f"Remaining: {int(item['km_remaining']):,} KM",
                                    size=10,
                                    color=ft.colors.GREY,
                                    font_family="Montserrat",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    f"Status: {item['status']}",
                                    size=10,
                                    color=ft.colors.GREEN if item["status"] == "Excellent" else (
                                        ft.colors.BLUE if item["status"] == "Good" else (
                                            ft.colors.ORANGE if item["status"] == "Fair" else ft.colors.RED
                                        )
                                    ),
                                    font_family="Montserrat",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ])
                        controls.append(
                            ft.GestureDetector(
                                on_tap=lambda e, name=item["name"]: page.go(
                                    f"/maintenance_detail/{vehicle_id}/{name}?username={username}&vehicle_name={vehicles[vehicle_index][1]['model']}"
                                ),
                                on_enter=on_item_enter,
                                on_exit=on_item_exit,
                                content=ft.Container(
                                    ref=container_ref,
                                    bgcolor="#f5f5f5",
                                    border_radius=10,
                                    #height=10,
                                    #width=10,
                                    padding=10,
                                    border=ft.border.all(2, ft.colors.GREY_300),
                                    ink=True,
                                    content=ft.Column(
                                        card_content,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=5
                                    )
                                ),
                                mouse_cursor=ft.MouseCursor.CLICK
                            )
                        )
                    except Exception as ex:
                        logging.error(
                            f"Error rendering maintenance card for vehicle {vehicle_id}, item {item.get('name', 'unknown')}: {str(ex)}")
                        continue
                maintenance_widgets[vehicle_id] = controls
                logging.info(f"Created new maintenance widgets for vehicle {vehicle_id}")

            car_components_section.current.content = ft.Column(
                scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.GridView(
                            runs_count=2,
                            max_extent=170,
                            spacing=10,
                            run_spacing=10,
                            child_aspect_ratio=1,
                            controls=controls
                        )
                    ]
            )

        def delete_vehicle(doc_id):
            nonlocal vehicle_index
            try:
                logging.info(f"Attempting to delete vehicle {doc_id}")
                db.collection("users").document(user_id).collection("vehicles").document(doc_id).delete()
                logging.info(f"Requested deletion of vehicle {doc_id}")
            except Exception as ex:
                error_message = ft.Text(f"Error deleting vehicle: {str(ex)}", color=ft.colors.RED, size=12,
                                        font_family="Montserrat")
                logging.error(f"Error deleting vehicle: {str(ex)}")
                page.controls.append(error_message)
                page.update()

        def show_delete_confirmation(doc_id):
            nonlocal vehicle_index
            logging.info(f"Showing delete confirmation for vehicle {doc_id}")
            if not vehicles or vehicle_index >= len(vehicles):
                logging.warning("No vehicles available for deletion or invalid vehicle_index")
                delete_confirmation.current.visible = False
                page.update()
                return

            idx = vehicle_index % len(vehicles)
            vehicle_model = vehicles[idx][1].get("model", "Unknown Vehicle")

            def on_yes_click(e):
                logging.info(f"Yes button clicked for vehicle {doc_id}")
                delete_vehicle(doc_id)
                delete_confirmation.current.visible = False
                page.update()

            def on_no_click(e):
                logging.info(f"No button clicked for vehicle {doc_id}")
                delete_confirmation.current.visible = False
                page.update()

            delete_confirmation.current.content = ft.Column([
                ft.Text(
                    f"ARE YOU SURE YOU WANT TO DELETE {vehicle_model}?",
                    size=16,
                    weight="bold",
                    color="#000000",
                    font_family="Montserrat",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Row([
                    ft.ElevatedButton(
                        text="Yes",
                        bgcolor="#3685cd",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            text_style=ft.TextStyle(font_family="Montserrat", size=14)
                        ),
                        on_click=on_yes_click
                    ),
                    ft.ElevatedButton(
                        text="No",
                        bgcolor="white",
                        color="#3685cd",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            text_style=ft.TextStyle(font_family="Montserrat", size=14)
                        ),
                        on_click=on_no_click
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            delete_confirmation.current.visible = True
            page.update()
            logging.info("Delete confirmation container displayed")

        def logout(page):
            page.client_storage.remove("user_id")
            page.client_storage.remove("cached_username")
            page.client_storage.remove("cached_vehicles")
            page.client_storage.remove("vehicles_last_updated")
            for vehicle_id in [v[0] for v in vehicles]:
                try:
                    page.client_storage.remove(f"maintenance_{vehicle_id}")
                except:
                    pass
            logging.info("User logged out")
            page.go("/login")

        main_content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(

                    content=ft.Stack([
                        ft.Column([
                            ft.Container(
                                ref=selected_car,
                                bgcolor="#e0e0e0",
                                border_radius=20,
                                padding=15,
                                margin=ft.margin.symmetric(horizontal=10, vertical=10),
                                content=ft.Text(""),
                                width = 350,
                                height=250,
                            ),
                            ft.Container(
                                ref=car_components_section,
                                visible=bool(vehicles),
                                border_radius=20,
                                width=370,

                                padding=10,
                                margin=ft.margin.only(top=-10, left=1, bottom=10),
                                height=400,
                                content=ft.Column(
                                    scroll=ft.ScrollMode.AUTO,
                                    controls=[
                                        ft.GridView(
                                            runs_count=2,
                                            max_extent=0,
                                            spacing=10,
                                            run_spacing=10,
                                            child_aspect_ratio=1.0,
                                            controls=[]
                                        )
                                    ]
                                )
                            )
                        ]),
                        ft.Container(
                            ref=delete_confirmation,
                            visible=False,
                            bgcolor="white",
                            border_radius=10,
                            padding=20,
                            width=300,
                            height=120,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                blur_radius=10,
                                spread_radius=2,
                                color=ft.colors.BLACK26
                            ),
                            top=200,
                            left=35,
                            clip_behavior=ft.ClipBehavior.NONE,
                            content=ft.Text("")
                        )
                    ])
                )
            ]
        )

        update_vehicle_display()

        view = ft.View(
            "/dashboard",
            controls=[
                ft.Stack([
                    ft.Container(
                        width=400,
                        height=820,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=["#1ca2bf", "#004f85", "#71a9cf"]
                        ),
                        padding=0,
                        margin=0,
                    ),
                    ft.Column([
                        ft.Row([header_wrapper], alignment=ft.MainAxisAlignment.CENTER),
                        main_content,
                    ],
                        width=400,
                        height=820)
                ],
                    width=400,
                    height=820)
            ],
            padding=0,
            bgcolor=ft.colors.TRANSPARENT,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        print(f"Total dashboard load time: {time.time() - start_page_time:.2f} seconds")
        logging.info(f"Dashboard load completed in {time.time() - start_page_time:.2f} seconds")
        return view

    except Exception as ex:
        logging.error(f"Error loading dashboard: {str(ex)}")
        return ft.View(
            "/dashboard",
            controls=[
                ft.Text("Unable to load dashboard. Please try again later.", color=ft.colors.RED,
                        font_family="Montserrat"),
                ft.ElevatedButton(
                    "Retry",
                    on_click=lambda e: page.go("/dashboard"),
                    bgcolor="#3685cd",
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=13),
                        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                    )
                ),
                ft.ElevatedButton(
                    "Go to Login",
                    on_click=lambda e: page.go("/login"),
                    bgcolor="#3685cd",
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=13),
                        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                    )
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )