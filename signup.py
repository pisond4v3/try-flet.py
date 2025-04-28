import flet as ft
from firebase_config import db, FIREBASE_API_KEY
import requests

# Shared logo widget
def logo_widget():
    return ft.Column([
        ft.Image(src="assets/AUTOCARE_LOGO.png", width=325, height=325, error_content=ft.Text("Logo not found")),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)

# Styled text field
def styled_text_field(label):
    field = ft.TextField(
        label=label,
        width=300,
        height=35,
        filled=True,
        bgcolor=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        color=ft.colors.BLUE_GREY_300,
        border_radius=ft.border_radius.all(20),
        border_color="#e8e8e8",  # Match background
        prefix_icon=ft.icons.PERSON,
    )

    def on_focus(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLACK, font_family="Montserrat")
        field.color = ft.colors.BLACK
        field.border_color = ft.colors.BLUE_500
        field.update()

    def on_blur(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat")
        field.color = ft.colors.BLUE_GREY_300
        field.border_color = "#e8e8e8"  # Match background
        field.update()

    field.on_focus = on_focus
    field.on_blur = on_blur

    return field

# Password field with eye toggle
def password_field(label_text):
    visible = False
    icon = ft.IconButton(icon=ft.icons.VISIBILITY_OFF)

    field = ft.TextField(
        label=label_text,
        width=300,
        height=35,
        password=True,
        suffix=icon,
        prefix_icon=ft.icons.LOCK,
        filled=True,
        bgcolor=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        color=ft.colors.BLUE_GREY_300,
        border_radius=ft.border_radius.all(20),
        border_color="#e8e8e8",  # Match background
    )

    def toggle_visibility(e):
        nonlocal visible
        visible = not visible
        field.password = not visible
        icon.icon = ft.icons.VISIBILITY if visible else ft.icons.VISIBILITY_OFF
        field.update()

    def on_focus(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLACK, font_family="Montserrat")
        field.color = ft.colors.BLACK
        field.border_color = ft.colors.BLUE_500
        field.update()

    def on_blur(e):
        field.label_style = ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat")
        field.color = ft.colors.BLUE_GREY_300
        field.border_color = "#e8e8e8"  # Match background
        field.update()

    icon.on_click = toggle_visibility
    field.on_focus = on_focus
    field.on_blur = on_blur

    return field

def signup_page(page: ft.Page):
    page.title = "AUTOCARE - Sign Up"
    page.window_width = 414
    page.window_height = 896

    # Theme settings from dashboard.py
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

    username = styled_text_field("Username")
    password = password_field("Password")
    confirm_password = password_field("Confirm Password")
    warning = ft.Text("", color=ft.colors.RED, font_family="Montserrat")

    def signup_user(email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)
        if response.ok:
            return response.json()["localId"]
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            raise Exception(error_message)

    def signup(e):
        warning.value = ""
        if not all([username.value, password.value, confirm_password.value]):
            warning.value = "Please fill out all fields."
            username.border_color = ft.colors.RED if not username.value else "#e8e8e8"
            password.border_color = ft.colors.RED if not password.value else "#e8e8e8"
            confirm_password.border_color = ft.colors.RED if not confirm_password.value else "#e8e8e8"
            page.update()
            return
        if password.value != confirm_password.value:
            warning.value = "Passwords do not match."
            password.border_color = ft.colors.RED
            confirm_password.border_color = ft.colors.RED
            page.update()
            return
        try:
            pseudo_email = f"{username.value}@autocare.com"
            user_id = signup_user(pseudo_email, password.value)
            db.collection("users").document(user_id).set({"username": username.value})
            page.client_storage.set("user_id", user_id)
            page.client_storage.set("cached_username", username.value)
            page.go("/dashboard")
        except Exception as e:
            error_detail = str(e).lower()
            if "email_already_exists" in error_detail:
                warning.value = "Username already exists. Please choose another."
                username.border_color = ft.colors.RED
            elif "weak_password" in error_detail:
                warning.value = "Password is too weak. Use at least 6 characters."
                password.border_color = ft.colors.RED
                confirm_password.border_color = ft.colors.RED
            elif "network" in error_detail:
                warning.value = "Network error. Please check your connection."
            else:
                warning.value = "Signup failed. Please try again later."
            page.update()

    def go_to_login(e):
        page.go("/login")

    # Main content
    main_content = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=400,
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Image(
                                src="assets/AUTOCARE SIGN-UP LOGO.jpg",
                                width=320,
                                height=150,
                                fit=ft.ImageFit.CONTAIN
                            ),
                            alignment=ft.alignment.top_center,
                            padding=0,
                            margin=ft.margin.only(top=0, bottom=10),
                        ),
                        ft.Container(
                            content=ft.Text("Sign up", size=22, weight=ft.FontWeight.BOLD, color="#3685cd",
                                            font_family="Montserrat"),
                            alignment=ft.alignment.top_left,
                            width=280
                        ),
                        username,
                        password,
                        confirm_password,
                        warning,
                        ft.ElevatedButton(
                            "Create Account",
                            on_click=signup,
                            width=280,
                            height=45,
                            bgcolor="#3685cd",
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                            )
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("ALREADY HAVE AN ACCOUNT?", weight=ft.FontWeight.BOLD, size=10,
                                            font_family="Montserrat"),
                                    ft.TextButton(
                                        "SIGN IN",
                                        on_click=go_to_login,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=10, weight=ft.FontWeight.BOLD, color="#3685cd",
                                                                    font_family="Montserrat")
                                        ),
                                    ),
                                ],
                            ),
                            margin=ft.margin.only(top=5),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                )
            )
        ]
    )

    return ft.View(
        "/signup",
        controls=[
            ft.Stack([
                ft.Container(
                    width=400,
                    height=800,
                    bgcolor="#e8e8e8",  # Match current background
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