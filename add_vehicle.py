import flet as ft
from firebase_config import db

# Styled text field with gradient-matched border
def styled_text_field(label):
    field = ft.TextField(
        label=label,
        width=300,
        filled=True,
        bgcolor=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        color=ft.colors.BLUE_GREY_300,
        border_radius=20,
        border_color="#004f85",  # Matches gradient color
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def on_focus(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLACK, font_family="Montserrat")
        field.color = ft.colors.BLACK
        field.border_color = ft.colors.BLUE_500
        field.update()

    def on_blur(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat")
        field.color = ft.colors.BLUE_GREY_300
        field.border_color = "#004f85"  # Matches gradient color
        field.update()

    field.on_focus = on_focus
    field.on_blur = on_blur
    return field

# Styled dropdown with gradient-matched border
def styled_dropdown(label, options):
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(option) for option in options],
        width=300,
        filled=True,
        bgcolor=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        text_style=ft.TextStyle(color=ft.colors.BLACK, font_family="Montserrat"),
        border_radius=20,
        border_color="#004f85",  # Matches gradient color
    )

def add_vehicle_page(page: ft.Page):
    page.title = "AUTOCARE - Add Vehicle"
    # Window size settings are typically set in main.py, but we'll keep them for consistency
    page.window_width = 414
    page.window_height = 896

    # Theme settings from autocare dashboard.py
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

    user_id = page.client_storage.get("user_id")
    if not user_id:
        return ft.View(
            "/add_vehicle",
            controls=[
                ft.Text("User not authenticated", color=ft.colors.RED, font_family="Montserrat"),
                ft.ElevatedButton(
                    "Go to Login",
                    on_click=lambda e: page.go("/login"),
                    width=300,
                    bgcolor="#3685cd",
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=13),
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                    )
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Fetch username
    try:
        user_doc = db.collection("users").document(user_id).get()
        username = user_doc.to_dict().get("username", f"User{user_id[-3:]}") if user_doc.exists else f"User{user_id[-3:]}"
    except Exception as ex:
        username = f"User{user_id[-3:]}"

    # Input fields
    model = styled_dropdown(
        "Choose your Car",
        ["Toyota Zenix", "Geely Coolray", "Toyota Wigo", "MG G50", "Hyundai Santa Fe"]
    )
    km_usage = styled_text_field("Current KM usage")
    car_age_months = styled_text_field("Age of your car (in months)")
    acceleration_braking = styled_dropdown(
        "Acceleration & Braking Style",
        ["Smooth", "Aggressive"]
    )
    trip_length = styled_dropdown(
        "Short Trips or Long Trips",
        ["Short Trips", "Long Trips"]
    )
    road_quality = styled_dropdown(
        "Road Quality",
        ["Smooth Paved roads", "Rough roads"]
    )
    climate_conditions = styled_dropdown(
        "Climate Conditions",
        ["Dry", "Wet"]
    )

    # Error message
    error_message = ft.Text("", color=ft.colors.RED, size=12, font_family="Montserrat")

    # Loading container reference
    loading_container = ft.Ref[ft.Container]()

    # Header from dashboard.py
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
                            padding=ft.padding.only(left=10,top=-5),
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
                                    spacing=5,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.LOGOUT,
                                            icon_color="#656262",
                                            icon_size=20,
                                            tooltip="Logout",
                                            on_click=lambda e: logout(page),
                                            padding=ft.padding.only(top=50)  # Lower the logout button
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.NOTIFICATIONS,
                                            icon_color="#656262",
                                            icon_size=20,
                                            tooltip="Notifications"
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
                            margin=ft.margin.only(left=10,top=-25),
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
                            margin=ft.margin.only(right=5,top=-25),
                        ),
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
            ], spacing=-5),
            bgcolor="#e8e8e8",
            padding=ft.padding.only(top=-5),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
            width=300,
        ),
        bgcolor="transparent",
        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
        width=370,
        height=125,
        margin=ft.margin.only(top=-23),
    )

    # Add vehicle function
    def add_vehicle(e):
        error_message.value = ""
        # Show loading screen
        if loading_container.current:
            loading_container.current.visible = True
            page.update()
        try:
            if not all([model.value, km_usage.value, car_age_months.value, acceleration_braking.value, trip_length.value,
                        road_quality.value, climate_conditions.value]):
                error_message.value = "Please fill out all fields."
                model.border_color = ft.colors.RED if not model.value else "#004f85"
                km_usage.border_color = ft.colors.RED if not km_usage.value else "#004f85"
                car_age_months.border_color = ft.colors.RED if not car_age_months.value else "#004f85"
                acceleration_braking.border_color = ft.colors.RED if not acceleration_braking.value else "#004f85"
                trip_length.border_color = ft.colors.RED if not trip_length.value else "#004f85"
                road_quality.border_color = ft.colors.RED if not road_quality.value else "#004f85"
                climate_conditions.border_color = ft.colors.RED if not climate_conditions.value else "#004f85"
                page.update()
                return
            km_usage_int = int(km_usage.value)
            car_age_months_int = int(car_age_months.value)
            if km_usage_int < 0:
                error_message.value = "KM Usage cannot be negative."
                km_usage.border_color = ft.colors.RED
                page.update()
                return
            if car_age_months_int < 0:
                error_message.value = "Car Age (Months) cannot be negative."
                car_age_months.border_color = ft.colors.RED
                page.update()
                return
            if car_age_months_int > 1200:
                error_message.value = "Car Age (Months) is too large."
                car_age_months.border_color = ft.colors.RED
                page.update()
                return

            vehicle_data = {
                "model": model.value,
                "km_usage": km_usage_int,
                "car_age_months": car_age_months_int,
                "driving_habits": {
                    "acceleration_braking": acceleration_braking.value,
                    "trip_length": trip_length.value,
                    "road_quality": road_quality.value,
                    "climate_conditions": climate_conditions.value
                }
            }
            db.collection("users").document(user_id).collection("vehicles").add(vehicle_data)
            page.client_storage.set("from_add_vehicle", True)  # Set flag for dashboard refresh
            page.go("/dashboard")
        except ValueError:
            error_message.value = "KM Usage and Car Age must be valid numbers."
            km_usage.border_color = ft.colors.RED
            car_age_months.border_color = ft.colors.RED
            page.update()
        except Exception as ex:
            error_message.value = f"Error adding vehicle: {str(ex)}"
            page.update()
        finally:
            # Hide loading screen
            if loading_container.current:
                loading_container.current.visible = False
                page.update()

    def logout(page):
        page.client_storage.remove("user_id")
        page.go("/login")

    # Main content
    main_content = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=370,

                content=ft.Column([
                    ft.Row([header_wrapper], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(
                        bgcolor="white",
                        border_radius=20,
                        padding=15,
                        margin=10,
                        content=ft.Column([
                            ft.Text("ADD YOUR VEHICLE", size=20, weight="bold", color="#004f85"),
                            error_message,
                            model,
                            km_usage,
                            car_age_months,
                            ft.Text("Driving Habits & Conditions:", size=16, weight="bold", color="#004f85"),
                            acceleration_braking,
                            trip_length,
                            road_quality,
                            climate_conditions,
                            ft.Container(
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(top=10),
                                content=ft.ElevatedButton(
                                    width=250,
                                    height=60,
                                    content=ft.Row([
                                        ft.Icon(name=ft.Icons.DIRECTIONS_CAR, color="white"),
                                        ft.Text("Add Vehicle", color="white")
                                    ], spacing=3, alignment=ft.MainAxisAlignment.CENTER),
                                    on_click=add_vehicle,
                                    style=ft.ButtonStyle(bgcolor="#3685cd", shape=ft.RoundedRectangleBorder(radius=20))
                                )
                            )
                        ], spacing=7)
                    )
                ], scroll=ft.ScrollMode.AUTO)
            )
        ]
    )

    # Layout
    return ft.View(
        "/add_vehicle",
        controls=[
            ft.Stack([
                ft.Container(
                    width=400,  # Match dashboard.py
                    height=800,  # Match dashboard.py
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#1ca2bf", "#004f85", "#71a9cf"]  # Same as dashboard.py
                    ),
                    padding=0,
                    margin=0,
                ),
                ft.Column([
                    main_content
                ],
                width=400,
                height=800)
            ],
            width=400,
            height=800)
        ],
        padding=0,
        bgcolor=ft.colors.TRANSPARENT,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )