import flet as ft
import pygetwindow as gw
import time
import threading

from login import login_page
from signup import signup_page
from dashboard import dashboard_page
from add_vehicle import add_vehicle_page
from maintenance_detail import maintenance_detail_page
from customer_service import customer_service_page
from automotive_news import automotive_news_page

def main(page: ft.Page):
    page.title = "AUTOCARE - Car Monitoring Assistant"
    page.padding = 0  # Remove padding to eliminate white outlines
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400  # Updated to 400
    page.window_height = 750  # Updated to 800
    page.window_resizable = False  # Best effort in Flet 0.19.0
    page.bgcolor = ft.colors.BLUE_900  # Fallback color to match gradient edge

    # Function to enforce window size and properties using pygetwindow
    def enforce_window_properties():
        while True:
            try:
                # Find the window by title
                windows = gw.getWindowsWithTitle("AUTOCARE - Car Monitoring Assistant")
                if not windows:
                    time.sleep(0.1)
                    continue
                window = windows[0]

                # Activate the window to ensure it can be manipulated
                try:
                    window.activate()  # Bring the window into focus
                    time.sleep(0.05)  # Small delay to ensure activation
                except Exception:
                    pass  # If activation fails, proceed anyway

                # Enforce size to 400x800
                if window.width != 400 or window.height != 750:
                    window.resizeTo(400, 750)

                # Center the window (optional)
                window.moveTo((window.screen.width - 400) // 2, (window.screen.height - 750) // 2)

                # Attempt to disable minimize/maximize (platform-dependent)
                if window.isMaximized:
                    window.restore()
                if window.isMinimized:
                    window.restore()

            except Exception as e:
                print(f"Error enforcing window properties: {e}")
                time.sleep(0.1)  # Retry quickly after an error
                continue

            time.sleep(0.1)  # Check more frequently (every 0.1 seconds)

    # Start a background thread to enforce window properties
    threading.Thread(target=enforce_window_properties, daemon=True).start()

    def route_change(e):
        page.views.clear()
        try:
            if page.route == "/login":
                view = login_page(page)
            elif page.route == "/signup":
                view = signup_page(page)
            elif page.route == "/dashboard":
                view = dashboard_page(page)
            elif page.route == "/add_vehicle":
                view = add_vehicle_page(page)
            elif page.route.startswith("/maintenance_detail/"):
                parts = page.route.split("/")
                if len(parts) >= 4:
                    vehicle_id = parts[2]
                    maintenance_name = parts[3]
                    view = maintenance_detail_page(page, vehicle_id, maintenance_name)
                else:
                    view = ft.View("/error", controls=[ft.Text("Invalid maintenance detail route", color=ft.Colors.RED)])
            elif page.route == "/customer_service":
                view = customer_service_page(page)
            elif page.route == "/automotive_news":
                view = automotive_news_page(page)
            else:
                view = ft.View("/error", controls=[ft.Text("Page not found", size=20, color=ft.Colors.RED)])

            # Check if the view is None and handle it
            if view is None:
                view = ft.View(
                    "/error",
                    controls=[ft.Text("Error: Page did not return a view. Contact developer.", color=ft.Colors.RED)]
                )
            page.views.append(view)

        except Exception as ex:
            page.views.append(ft.View("/error", controls=[ft.Text(f"Error loading page: {str(ex)}", color=ft.Colors.RED)]))
        page.update()

    page.on_route_change = route_change

    user_id = page.client_storage.get("user_id")
    if user_id:
        page.go("/dashboard")
    else:
        page.go("/login")

ft.app(
    target=main,
    assets_dir="assets",
)