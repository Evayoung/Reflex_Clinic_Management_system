import reflex as rx
from ..states.auth_state import UserAuthState

def index_nav():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(src="/school_logo.png", height="40px", margin_right="10px", margin_left="1rem"),
                rx.text(
                    "University Of Ilorin",
                    font_size="1.7rem",
                    font_weight="bold",
                    color="white",
                    text_align=rx.breakpoints(sm="center", md="left"),
                ),
            ),

            rx.hstack(
                rx.button(
                    "Home",
                    cursor="pointer",
                    color="white",
                    bg="transparent",
                    position="relative",
                    padding_bottom="0.5rem",
                    on_click=UserAuthState.change_main_view("Home"),
                    _after={
                        "content": '""',
                        "position": "absolute",
                        "width": "100%",
                        "height": "3px",  # Thickness of the border
                        "bottom": "0",
                        "left": "0",
                        "background": "#e67e22",  # Dark orange color
                        "transform": "scaleX(0)",  # Start with no border
                        "transform_origin": "left",
                        "transition": "transform 0.3s ease",
                    },
                    _hover={
                        "color": "white",
                        "bg": "transparent",
                        "_after": {
                            "transform": "scaleX(1)",  # Full border on hover
                            "transform_origin": "left",
                        }
                    },
                ),
                rx.button(
                    "News",
                    cursor="pointer",
                    color="white",
                    bg="transparent",
                    position="relative",
                    padding_bottom="0.5rem",
                    on_click=UserAuthState.change_main_view("News"),
                    _after={
                        "content": '""',
                        "position": "absolute",
                        "width": "100%",
                        "height": "3px",
                        "bottom": "0",
                        "left": "0",
                        "background": "#e67e22",
                        "transform": "scaleX(0)",
                        "transform_origin": "left",
                        "transition": "transform 0.3s ease",
                    },
                    _hover={
                        "color": "white",
                        "bg": "transparent",
                        "_after": {
                            "transform": "scaleX(1)",
                            "transform_origin": "left",
                        }
                    },
                ),
                rx.button(
                    "About Us",
                    cursor="pointer",
                    color="white",
                    bg="transparent",
                    position="relative",
                    padding_bottom="0.5rem",
                    on_click=UserAuthState.change_main_view("About"),
                    _after={
                        "content": '""',
                        "position": "absolute",
                        "width": "100%",
                        "height": "3px",
                        "bottom": "0",
                        "left": "0",
                        "background": "#e67e22",
                        "transform": "scaleX(0)",
                        "transform_origin": "left",
                        "transition": "transform 0.3s ease",
                    },
                    _hover={
                        "color": "white",
                        "bg": "transparent",
                        "_after": {
                            "transform": "scaleX(1)",
                            "transform_origin": "left",
                        }
                    },
                ),
                align="center",
                justify="end",
            ),
            justify="between",
            align="center",
            padding="1rem",
            width="100%",
            position="fixed",
            top="0",
            spacing="4",
            z_index="1000",
        ),
    )

def main_nav():
    return rx.box(
        rx.hstack(
            rx.image(src="/school_logo.png", height="40px", margin_right="10px", margin_left="1rem"),
            rx.hstack(
                rx.desktop_only(
                    rx.box(
                        rx.button(
                            "Home",
                            cursor="pointer",
                            color="#00303A",
                            bg="rgba(255, 255, 255, 0.1)",
                            on_click=rx.redirect('/student/home')
                        ),
                        rx.button(
                            "Schedule",
                            cursor="pointer",
                            color="#00303A",
                            bg="rgba(255, 255, 255, 0.1)",
                            on_click=rx.redirect("/student/schedule")
                        ),
                        rx.button(
                            "Appointment",
                            cursor="pointer",
                            color="#00303A",
                            bg="rgba(255, 255, 255, 0.1)",
                            on_click=rx.redirect("/student/appointment")
                        ),
                        rx.button(
                            "Records",
                            cursor="pointer",
                            color="#00303A",
                            bg="rgba(255, 255, 255, 0.1)",
                            on_click=rx.redirect("/student/records")
                        ),
                        rx.button(
                            "Prescription",
                            cursor="pointer",
                            color="#00303A",
                            bg="rgba(255, 255, 255, 0.1)",
                            on_click=rx.redirect("/student/prescription")
                        ),
                    ),
                ),

                rx.mobile_and_tablet(
                    rx.icon(
                        "menu",
                        cursor="pointer",
                        color="#00303A",
                    ),
                ),

                spacing="6",  # Space out the buttons
                margin_right="1rem",  # Add margin to the right of the buttons
                padding=".4rem",
                padding_left="2rem",
                padding_right="2rem",
                # border_radius="2px",
                # background_color="rgba(255, 255, 255, 0.1)",
                # box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
            ),

            justify_content="space-between",  # Space out the logo and buttons
            align_items="center",  # Center items vertically
            padding="1rem",
            width="100%",
            position="fixed",
            top="0",
            z_index="1000",
            background_color="#ffffff",
            box_shadow="0 2px 4px rgba(0,0,0,0.1)",
            border_buttom="1px solid #330099",
        ),
    )


def staff_nav():
    return rx.box(
        rx.hstack(
            rx.text(
                "University Of Ilorin Staffs",
                font_size="2rem",
                font_weight="bold",
                color="#330099",
                text_align="center",
                # text_align=rx.breakpoints(sm="center", md="left"),
            ),

            justify_content="center",  # Space out the logo and buttons
            align_items="center",  # Center items vertically
            padding="1rem",
            width="100%",
            position="fixed",
            top="0",
            spacing="4",
            z_index="1000",
            # background_color="#ffffff",
            # box_shadow="0 2px 4px rgba(0,0,0,0.5)",
        ),
    )
