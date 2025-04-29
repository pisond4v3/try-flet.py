import flet as ft
from firebase_config import db

def customer_service_page(page: ft.Page):
    page.title = "AUTOCARE - Customer Service"
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
            "/customer_service",
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
            "Drift Xaust": "https://www.driftxaust.com/",
            "Goodyear Servitek": "https://www.goodyear.com.ph/store/goodyear-servitek-quezon-avenue",
            "Motech": "https://motech.ph/",
            "Yock’s Auto Electrical Repair Shop": "https://www.facebook.com/YocksAutoElectrical/",
            "Notorious Motorsports": "https://www.facebook.com/notoriousmotorsports/",
            "V-MAC Car Display": "https://www.facebook.com/allenjoseph.diez.52/",
            "Rapide Auto Service – Car Repair": "https://rapide.ph/",
            "Tsikot Forums": "https://www.tsikot.com/forums/",
            "Automotive Forums": "https://www.automotiveforums.com/",
            "Community Cartalk": "https://community.cartalk.com/",
            "Edmunds Forums": "https://forums.edmunds.com/"
        }.get(e.control.content.value)
        if url:
            page.launch_url(url)

    tab_mechanic_text = ft.Text(
        "FINDING A MECHANIC?",
        size=12,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_700,
        font_family="Montserrat",
    )
    tab_community_text = ft.Text(
        "ASK THE COMMUNITY",
        size=12,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_400,
        font_family="Montserrat",
    )

    # Underline indicators
    underline_mechanic = ft.Container(height=2, width=120, bgcolor=ft.colors.BLUE_700, visible=True)
    underline_community = ft.Container(height=2, width=120, bgcolor=ft.colors.BLUE_700, visible=False)

    def switch_tab(tab_name):
        if tab_name == "mechanic" and content_container.controls != mechanic_page.controls:
            content_container.controls = mechanic_page.controls
            tab_mechanic_text.color = ft.colors.BLUE_700
            tab_community_text.color = ft.colors.BLUE_400
            underline_mechanic.visible = True
            underline_community.visible = False
        elif tab_name == "community" and content_container.controls != community_page.controls:
            content_container.controls = community_page.controls
            tab_mechanic_text.color = ft.colors.BLUE_400
            tab_community_text.color = ft.colors.BLUE_700
            underline_mechanic.visible = False
            underline_community.visible = True
        page.update()

    # Tab switcher
    tab_switcher = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=tab_mechanic_text,
                            on_click=lambda _: switch_tab("mechanic"),
                            margin=ft.margin.only(left=-15),
                        ),
                        underline_mechanic,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
                ft.Column(
                    controls=[
                        ft.Container(
                            content=tab_community_text,
                            on_click=lambda _: switch_tab("community"),
                            alignment=ft.alignment.center,
                        ),
                        underline_community,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            expand=True,
        ),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
    )

    # Page 1: Recommended Mechanics
    mechanic_buttons = [
        ft.ElevatedButton(
            content=ft.Text("Drift Xaust", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Goodyear Servitek", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Motech", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Yock’s Auto Electrical Repair Shop", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Notorious Motorsports", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("V-MAC Car Display", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Rapide Auto Service – Car Repair", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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

    mechanic_page = ft.Column(
        controls=mechanic_buttons,
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Page 2: Community Forums
    community_buttons = [
        ft.ElevatedButton(
            content=ft.Text("Tsikot Forums", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Automotive Forums", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Community Cartalk", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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
            content=ft.Text("Edmunds Forums", size=14, weight=ft.FontWeight.BOLD, font_family="Montserrat"),
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

    community_page = ft.Column(
        controls=community_buttons,
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Dynamic container for page switching
    content_container = ft.Column(
        controls=mechanic_page.controls,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Header container (restored from original customer_service.py)
    header_container = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, icon_color=ft.colors.BLUE_700, on_click=go_back),
            ft.Text(
                "CUSTOMER SERVICE",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_700,
                font_family="Montserrat",
            ),
            ft.Icon(ft.icons.SUPPORT_AGENT, color=ft.colors.BLUE_700),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#e8e8e8",
        border_radius=10,
        padding=ft.padding.all(15),
        width=340,  # Match view width to avoid spaces
        margin=ft.margin.only(left=-14,top=10),
    )

    # Content container for tabs and buttons
    content_inner_container = ft.Container(
        content=ft.Column([
            tab_switcher,
            content_container,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#e8e8e8",
        border_radius=10,
        padding=ft.padding.all(15),
        width=350,
        height=600, # Match header width
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
        "/customer_service",
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
                    main_content
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