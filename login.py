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
        bgcolor="#e8e8e8",
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        color=ft.colors.BLUE_GREY_300,
        border_radius=ft.border_radius.all(20),
        border_color=ft.colors.WHITE,
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
        field.border_color = ft.colors.WHITE
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
        bgcolor="#e8e8e8",
        label_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300, font_family="Montserrat"),
        color=ft.colors.BLUE_GREY_300,
        border_radius=ft.border_radius.all(20),
        border_color=ft.colors.WHITE,
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
        field.border_color = ft.colors.WHITE
        field.update()

    icon.on_click = toggle_visibility
    field.on_focus = on_focus
    field.on_blur = on_blur

    return field

def login_page(page: ft.Page):
    username = styled_text_field("Username")
    password = password_field("Password")
    warning = ft.Text("", color=ft.colors.RED, font_family="Montserrat")
    loading_container = ft.Ref[ft.Container]()

    def login_user(email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)
        if response.ok:
            return response.json()["localId"]
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            raise Exception(error_message)

    def login(e):
        warning.value = ""
        # Show loading screen
        if loading_container.current:
            loading_container.current.visible = True
            page.update()
        try:
            if not username.value or not password.value:
                warning.value = "Please enter both username and password."
                username.border_color = ft.colors.RED
                password.border_color = ft.colors.RED
                page.update()
                return
            pseudo_email = f"{username.value}@autocare.com"
            user_id = login_user(pseudo_email, password.value)
            page.client_storage.set("user_id", user_id)
            page.client_storage.set("cached_username", username.value)
            page.go("/dashboard")
        except Exception as e:
            error_detail = str(e).lower()
            if "email_not_found" in error_detail or "invalid_email" in error_detail:
                warning.value = "Username not found. Please check your username."
                username.border_color = ft.colors.RED
            elif "invalid_password" in error_detail:
                warning.value = "Incorrect password. Please try again."
                password.border_color = ft.colors.RED
            elif "too_many_attempts" in error_detail:
                warning.value = "Too many attempts. Try again later."
            elif "network" in error_detail:
                warning.value = "Network error. Please check your connection."
            else:
                warning.value = "Login failed. Wrong username/password."
            page.update()
        finally:
            # Hide loading screen
            if loading_container.current:
                loading_container.current.visible = False
                page.update()

    def go_to_signup(e):
        page.go("/signup")

    # Create a full-screen gradient container
    gradient_container = ft.Container(
        width=400,
        height=820,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#1ca2bf", "#004f85", "#71a9cf"]
        ),
        padding=0,
        margin=0,
    )

    # Stack the gradient behind the content
    content = ft.Stack([
        gradient_container,
        ft.Column([
            ft.Container(
                content=logo_widget(),
                width=340,
                height=350,
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.all(25),
                bgcolor="#e8e8e8",
                margin=5,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("SIGN IN", size=20, weight=ft.FontWeight.BOLD, color="#3685cd", font_family="Montserrat"),
                        alignment=ft.alignment.center_left,
                        width=250,
                    ),
                    username,
                    password,
                    warning,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Login",
                            on_click=login,
                            width=250,
                            height=40,
                            bgcolor="#3685cd",
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, font_family="Montserrat")
                            )
                        ),
                        margin=ft.margin.only(top=5),
                    ),
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("DON'T HAVE AN ACCOUNT?", weight=ft.FontWeight.BOLD, size=10,
                                        font_family="Montserrat"),
                                ft.TextButton(
                                    "SIGN UP",
                                    on_click=go_to_signup,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=10, weight=ft.FontWeight.BOLD,
                                                                color="#3685cd", font_family="Montserrat")
                                    ),
                                ),
                            ]
                        ),
                        margin=ft.margin.only(top=5),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=320,
                height=280,
                padding=5,
                border_radius=18,
                bgcolor="#e8e8e8",
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        height=820,  # Match window height
        width=400,   # Match window width
        ),
        ft.Container(
            ref=loading_container,
            visible=False,
            bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK54),
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.ProgressRing(color="#3685cd", width=50, height=50),
                ft.Text("Logging In...", color=ft.colors.WHITE, size=16, font_family="Montserrat", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            width=400,
            height=820,
        )
    ],
    width=400,
    height=820)

    return ft.View(
        "/login",
        controls=[content],
        padding=0,
        bgcolor=ft.colors.TRANSPARENT,
        vertical_alignment=ft.MainAxisAlignment.START,  # Align view content to the top
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )