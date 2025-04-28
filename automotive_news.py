import flet as ft
from firebase_config import db

def automotive_news_page(page: ft.Page):
    page.title = "AUTOCARE - Automotive News"
    # Window size settings are typically set in main.py, but we'll keep them for consistency
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

    user_id = page.client_storage.get("user_id")
    if not user_id:
        return ft.View(
            "/automotive_news",
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

    def go_back(e):
        page.go("/dashboard")

    def open_link(e):
        url = {
            "CarGuide.PH": "https://www.carguide.ph/search/label/News",
            "Top Gear Philippines": "https://www.topgear.com.ph/",
            "ZIGWHEELS": "https://www.zigwheels.ph/car-news",
            "Autoindustriya.com": "https://www.autoindustriya.com/",
            "Autocar Philippines": "https://autocar.com.ph/",
            "Automotive News": "https://www.autonews.com/",
            "Reuters": "https://www.reuters.com/business/autos-transportation/",
            "MOTORTREND": "https://www.motortrend.com/auto-news/"
        }.get(e.control.content.value)
        if url:
            page.launch_url(url)

    # Header container
    header_container = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, icon_color=ft.colors.BLUE_700, on_click=go_back),
            ft.Text(
                "AUTOMOTIVE NEWS",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_700,
                font_family="Montserrat",
            ),
            ft.Icon(ft.icons.ARTICLE, color=ft.colors.BLUE_700),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#e8e8e8",
        border_radius=10,
        padding=ft.padding.all(15),
        width=340,  # Match view width to avoid spaces
        margin=ft.margin.only(left=-14, top=10),
    )

    # News buttons
    news_buttons = [
        ft.ElevatedButton(
            content=ft.Text("CarGuide.PH", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("Top Gear Philippines", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("ZIGWHEELS", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("Autoindustriya.com", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("Autocar Philippines", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("Automotive News", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("Reuters", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
        ft.ElevatedButton(
            content=ft.Text("MOTORTREND", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            on_click=open_link,
            width=300,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Montserrat"),
            ),
        ),
    ]

    # Dynamic container for buttons
    content_container = ft.Column(
        controls=news_buttons,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # Content container for buttons
    content_inner_container = ft.Container(
        content=ft.Column([
            content_container,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#e8e8e8",
        border_radius=10,
        padding=ft.padding.all(15),
        width=350,
        height=600,  # Match header width
        margin=ft.margin.only(left=18),
    )

    # Main content
    main_content = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=400,
                content=ft.Column([
                    ft.Row([header_container], alignment=ft.MainAxisAlignment.CENTER),
                    content_inner_container,
                ], scroll=ft.ScrollMode.AUTO)
            )
        ]
    )

    return ft.View(
        "/automotive_news",
        controls=[
            ft.Stack([
                ft.Container(
                    width=400,
                    height=800,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#1ca2bf", "#004f85", "#71a9cf"]
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