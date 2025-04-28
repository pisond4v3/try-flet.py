import flet as ft
from firebase_config import db
import logging
from datetime import datetime
from utils import calculate_status_and_schedule, COMPONENT_DATA

logging.basicConfig(filename="maintenance_detail.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Maintenance items for fallback image paths (mirroring dashboard.py)
MAINTENANCE_ITEMS = [
    {"name": "Engine Oil & Oil Filter", "image": "assets/maintenance_icon/engine_oil.png"},
    {"name": "Air Filter", "image": "assets/maintenance_icon/air_filter.png"},
    {"name": "Tires", "image": "assets/maintenance_icon/tires.png"},
    {"name": "Transmission Fluid", "image": "assets/maintenance_icon/transmission_fluid.png"},
    {"name": "Fuel Filter", "image": "assets/maintenance_icon/fuel_filter.png"},
    {"name": "Coolant (Radiator Fluid)", "image": "assets/maintenance_icon/coolant.png"},
    {"name": "Battery", "image": "assets/maintenance_icon/battery.png"},
    {"name": "Brake Fluid and Pads", "image": "assets/maintenance_icon/brake_fluids-and_pads.png"},
]

def validate_date(date_str: str) -> datetime:
    if not date_str or date_str == "N/A":
        logging.info(f"Empty or N/A date string: {date_str}")
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

def maintenance_detail_page(page: ft.Page, vehicle_id: str, component_name: str):
    # Clean up component_name to ensure it matches COMPONENT_DATA keys
    component_name = component_name.split("?")[0].strip()
    page.title = f"AUTOCARE - {component_name}"
    page.window_width = 414
    page.window_height = 896
    logging.info(f"Loading maintenance detail for {component_name}, vehicle {vehicle_id}")

    # Parse query parameters from the route
    route = page.route
    query_params = {}
    if "?" in route:
        query_string = route.split("?")[1]
        for param in query_string.split("&"):
            key, value = param.split("=")
            query_params[key] = value

    # Extract username and vehicle_name from query parameters
    username = query_params.get("username", page.client_storage.get("cached_username") or "Unknown User")
    vehicle_name = query_params.get("vehicle_name", "Unknown Vehicle")

    # Fetch maintenance data
    maintenance_ref = db.collection("users").document(page.client_storage.get("user_id")).collection("vehicles").document(vehicle_id).collection("maintenance").document(component_name)
    maintenance_doc = maintenance_ref.get()
    maintenance_data = maintenance_doc.to_dict() if maintenance_doc.exists else {
        "status": "N/A",
        "last_maintenance_date": "N/A",
        "estimated_maintenance_schedule": "N/A",
        "component_type": None,
        "km_remaining": 0,
        "prediction_reasons": [],
        "last_maintenance_km": 0
    }

    # Get component options and set initial component_type
    component_types = COMPONENT_DATA.get(component_name, {}).get("options", [])
    logging.info(f"Component types for {component_name}: {component_types}")
    initial_component_type = maintenance_data.get("component_type")
    if not initial_component_type and component_types:
        initial_component_type = component_types[0]
        maintenance_data["component_type"] = initial_component_type
        maintenance_ref.set(maintenance_data, merge=True)
        logging.info(f"Set default component_type for {component_name}: {initial_component_type}")

    # Determine initial image path
    component_key = initial_component_type or "default"
    image_path = COMPONENT_DATA.get(component_name, {}).get("images", {}).get(component_key, None)
    if not image_path:
        item = next((i for i in MAINTENANCE_ITEMS if i["name"] == component_name), None)
        image_path = item["image"] if item else "assets/maintenance_icon/default.png"
    logging.info(f"Initial image for {component_name}: {image_path}")

    # Create refs for dynamic updates
    component_image = ft.Ref[ft.Image]()
    selected_component_type = ft.Ref[ft.Dropdown]()
    last_maintenance_date_ref = ft.Ref[ft.Text]()

    def open_date_picker():
        def on_date_select(e):
            selected_date = date_picker.value
            if selected_date:
                update_maintenance_date(selected_date)
            close_dialog()

        def close_dialog():
            page.overlay.remove(date_picker)
            page.update()

        date_picker = ft.DatePicker(
            on_change=on_date_select,
            first_date=datetime(2000, 1, 1),
            last_date=datetime.now(),
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR,
            confirm_text="OK",
            cancel_text="Cancel",
        )
        logging.info("Opening date picker")
        page.overlay.append(date_picker)
        page.update()
        date_picker.open = True
        page.update()

    def update_maintenance_date(date):
        if date > datetime.now():
            page.controls.append(ft.Text("Cannot set future date", color=ft.colors.RED, font_family="Montserrat"))
            page.update()
            return
        formatted_date = date.strftime("%m/%d/%Y")
        maintenance_data["last_maintenance_date"] = formatted_date
        logging.info(f"Updated last_maintenance_date to {formatted_date}")

        vehicle_doc = db.collection("users").document(page.client_storage.get("user_id")).collection("vehicles").document(vehicle_id).get()
        vehicle_data = vehicle_doc.to_dict() if vehicle_doc.exists else {}
        current_km = vehicle_data.get("km_usage", 0)
        maintenance_data["last_maintenance_km"] = current_km
        logging.info(f"Stored last_maintenance_km: {current_km}")

        last_maintenance_date_ref.current.value = formatted_date
        page.update()

        km_since_last = current_km - maintenance_data.get("last_maintenance_km", 0)
        adjusted_vehicle_data = vehicle_data.copy()
        adjusted_vehicle_data["km_usage"] = km_since_last

        status, estimated_schedule, km_remaining, reasons = calculate_status_and_schedule(
            adjusted_vehicle_data, component_name, formatted_date, maintenance_data.get("component_type")
        )
        maintenance_data.update({
            "status": status,
            "estimated_maintenance_schedule": estimated_schedule,
            "km_remaining": km_remaining,
            "prediction_reasons": reasons
        })
        maintenance_ref.set(maintenance_data, merge=True)
        update_ui()

    def update_component_type(e):
        new_component_type = selected_component_type.current.value
        maintenance_data["component_type"] = new_component_type
        logging.info(f"Updated component_type for {component_name} to {new_component_type}")

        component_key = new_component_type or "default"
        new_image_path = COMPONENT_DATA.get(component_name, {}).get("images", {}).get(component_key, None)
        if not new_image_path:
            item = next((i for i in MAINTENANCE_ITEMS if i["name"] == component_name), None)
            new_image_path = item["image"] if item else "assets/maintenance_icon/default.png"
        component_image.current.src = new_image_path
        logging.info(f"Updated image for {component_name} to {new_image_path}")

        if maintenance_data.get("last_maintenance_date") != "N/A":
            vehicle_doc = db.collection("users").document(page.client_storage.get("user_id")).collection("vehicles").document(vehicle_id).get()
            vehicle_data = vehicle_doc.to_dict() if vehicle_doc.exists else {}
            km_since_last = vehicle_data.get("km_usage", 0) - maintenance_data.get("last_maintenance_km", 0)
            adjusted_vehicle_data = vehicle_data.copy()
            adjusted_vehicle_data["km_usage"] = km_since_last

            status, estimated_schedule, km_remaining, reasons = calculate_status_and_schedule(
                adjusted_vehicle_data, component_name, maintenance_data["last_maintenance_date"], new_component_type
            )
            maintenance_data.update({
                "status": status,
                "estimated_maintenance_schedule": estimated_schedule,
                "km_remaining": km_remaining,
                "prediction_reasons": reasons
            })
        maintenance_ref.set(maintenance_data, merge=True)
        update_ui()

    def update_ui():
        status_text.current.value = f"Status: {maintenance_data.get('status', 'N/A')}"
        status_text.current.color = (
            ft.colors.GREEN if maintenance_data.get("status") == "Excellent" else
            ft.colors.BLUE if maintenance_data.get("status") == "Good" else
            ft.colors.ORANGE if maintenance_data.get("status") == "Fair" else
            ft.colors.RED
        )
        estimated_schedule_text.current.value = maintenance_data.get("estimated_maintenance_schedule", "N/A")
        page.update()

    def show_component_definition(e):
        selected_type = selected_component_type.current.value or "default"
        definition = COMPONENT_DATA.get(component_name, {}).get("definitions", {}).get(selected_type, "No definition available.")
        dialog = ft.AlertDialog(
            title=ft.Text(f"{selected_type} Definition", font_family="Montserrat"),
            content=ft.Text(definition, font_family="Montserrat"),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_definition_dialog())
            ]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
        logging.info(f"Displayed definition for {selected_type}: {definition}")

    def close_definition_dialog():
        page.dialog.open = False
        page.update()

    def go_back(e):
        page.go("/dashboard")

    # UI Components
    status_text = ft.Ref[ft.Text]()
    estimated_schedule_text = ft.Ref[ft.Text]()

    last_maintenance_date_button = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name=ft.Icons.CALENDAR_TODAY, size=20, color="white"),
            ft.Text(
                ref=last_maintenance_date_ref,
                value=maintenance_data.get("last_maintenance_date", "N/A"),
                size=14,
                font_family="Montserrat",
                color="white",
                weight=ft.FontWeight.NORMAL
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        style=ft.ButtonStyle(
            bgcolor="#3685cd",
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
        width=200,
        height=40,
        on_click=lambda e: open_date_picker(),
    )

    if maintenance_data.get("last_maintenance_date") == "N/A":
        date_prompt_dialog = ft.AlertDialog(
            title=ft.Text("Missing Maintenance Date", font_family="Montserrat"),
            content=ft.Text("Please provide the last maintenance date for accurate scheduling.", font_family="Montserrat"),
            actions=[
                ft.TextButton("Set Date", on_click=lambda e: open_date_picker()),
                ft.TextButton("Cancel", on_click=lambda e: go_back(None))
            ],
            open=True
        )
        page.dialog = date_prompt_dialog
        page.update()

    component_type_dropdown = ft.Dropdown(
        ref=selected_component_type,
        options=[ft.dropdown.Option(opt) for opt in component_types],
        value=initial_component_type,
        width=200,
        bgcolor="white",
        border_radius=10,
        text_style=ft.TextStyle(font_family="Montserrat", size=14),
        on_change=update_component_type,
        visible=bool(component_types)
    )

    info_icon = ft.IconButton(
        icon=ft.Icons.INFO_OUTLINE,
        icon_color="white",
        on_click=show_component_definition,
        visible=bool(component_types),
        tooltip="View component type definition"
    )

    view = ft.View(
        "/maintenance_detail",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#1c77bf",
                margin=ft.margin.all(20),
                content=ft.Column([
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=go_back
                            ),
                            ft.Text(
                                username,
                                size=16,
                                color="white",
                                font_family="Montserrat"
                            ),
                            ft.IconButton(
                                icon=ft.Icons.NOTIFICATIONS,
                                icon_color="white"
                            )
                        ],
                        spacing=10
                    ),
                    ft.Image(
                        ref=component_image,
                        src=image_path if image_path else "assets/maintenance_icon/default.png",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Icon(ft.Icons.BUILD, color="#fdd835", size=50)
                    ),
                    ft.Container(
                        bgcolor="white",
                        border_radius=10,
                        content=ft.Column([
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(name=ft.Icons.BUILD, color="#1c77bf", size=30),
                                    ft.Text(
                                        component_name,
                                        size=20,
                                        weight="bold",
                                        color="#1c77bf",
                                        font_family="Montserrat"
                                    )
                                ],
                                spacing=10
                            ),
                            ft.Text(
                                "Last Maintenance Date",
                                size=14,
                                color="black",
                                font_family="Montserrat"
                            ),
                            last_maintenance_date_button,
                            ft.Text(
                                "Choose your Car’s components:",
                                size=14,
                                color="black",
                                font_family="Montserrat",
                                visible=bool(component_types)
                            ),
                            ft.Row(
                                controls=[
                                    component_type_dropdown,
                                    info_icon
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5
                            ),
                            ft.Text(
                                "Estimated Maintenance Schedule:",
                                size=14,
                                color="black",
                                font_family="Montserrat"
                            ),
                            ft.ElevatedButton(
                                content=ft.Text(
                                    ref=estimated_schedule_text,
                                    value=maintenance_data.get("estimated_maintenance_schedule", "N/A"),
                                    size=14,
                                    color="white",
                                    font_family="Montserrat"
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor="#3685cd",
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                ),
                                width=200,
                                height=40,
                                disabled=True
                            ),
                            ft.Text(
                                ref=status_text,
                                value=f"Status: {maintenance_data.get('status', 'N/A')}",
                                size=14,
                                color=(
                                    ft.colors.GREEN if maintenance_data.get("status") == "Excellent" else
                                    ft.colors.BLUE if maintenance_data.get("status") == "Good" else
                                    ft.colors.ORANGE if maintenance_data.get("status") == "Fair" else
                                    ft.colors.RED
                                ),
                                font_family="Montserrat"
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                    )
                ], alignment=ft.MainAxisAlignment.START, spacing=20)
            )
        ]
    )
    return view