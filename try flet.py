import flet as ft

def main(page: ft.Page):
    page.title = "Customer Service"
    page.bgcolor = "#004f85"
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_frameless = True

    # Track which tab is active
    current_tab = ft.Ref[ft.Container]()

    def switch_tab(tab_name):
        if tab_name == "mechanic" and content_container.controls != mechanic_page.controls:
            content_container.controls = mechanic_page.controls
            tab_mechanic_text.color = "blue"
            tab_community_text.color = "#656262"
            underline_mechanic.visible = True
            underline_community.visible = False
        elif tab_name == "community" and content_container.controls != community_page.controls:
            content_container.controls = community_page.controls
            tab_mechanic_text.color = "#656262"
            tab_community_text.color = "blue"
            underline_mechanic.visible = False
            underline_community.visible = True
        page.update()

    # Header bar
    header = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color="white", icon_size=25),
                ft.Text("CUSTOMER SERVICE", color="white", weight=ft.FontWeight.BOLD, size=18),
                ft.Icon(ft.icons.SUPPORT_AGENT, color="white", size=25),
            ]
        ),
        padding=ft.padding.all(15),
    )

    # Tab switcher
    tab_mechanic_text = ft.Text("FINDING A MECHANIC?", weight=ft.FontWeight.BOLD, color="blue")
    tab_community_text = ft.Text("ASK THE COMMUNITY", weight=ft.FontWeight.BOLD, color="#656262")

    underline_mechanic = ft.Container(height=2, width=130, bgcolor="blue", visible=True)
    underline_community = ft.Container(height=2, width=130, bgcolor="blue", visible=False)

    tab_switcher = ft.Container(
        content=ft.Column([
            ft.Row(
                controls=[
                    ft.Container(
                        content=tab_mechanic_text,
                        on_click=lambda _: switch_tab("mechanic")
                    ),
                    ft.Container(
                        content=tab_community_text,
                        on_click=lambda _: switch_tab("community")
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            ft.Row([
                ft.Container(content=underline_mechanic, alignment=ft.alignment.center),
                ft.Container(content=underline_community, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ]),
        padding=10
    )

    # Page 1: Recommended Mechanics
    mechanic_buttons = [
        ft.ElevatedButton("RECOMMENDED 1", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("RECOMMENDED 2", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("RECOMMENDED 3", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("RECOMMENDED 4", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("RECOMMENDED 5", bgcolor="#3685cd", color="white", width=300),
    ]

    mechanic_page = ft.Column(controls=mechanic_buttons, spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    # Page 2: Community Forums
    community_buttons = [
        ft.ElevatedButton("Tsikot Forums", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("Automative Forums", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("Community Cartalk", bgcolor="#3685cd", color="white", width=300),
        ft.ElevatedButton("Edmunds Forums", bgcolor="#3685cd", color="white", width=300),
    ]

    community_page = ft.Column(controls=community_buttons, spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    # Dynamic container for page switching
    content_container = ft.Column(
        controls=mechanic_page.controls,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # Main layout
    page.add(
        ft.Container(
            content=ft.Column([
                header,
                tab_switcher,
                content_container
            ],
            spacing=20),
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1ca2bf", "#004f85", "#71a9cf"],
                stops=[0.0, 0.5, 1.0]
            ),
            border_radius=15,
            width=414,
            height=896
        )
    )


ft.app(target=main)
