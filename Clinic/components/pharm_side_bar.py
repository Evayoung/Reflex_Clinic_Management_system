import reflex as rx
from ..states import pharmercist_state



nav_style = dict(
    padding=".7em",
    text_align="left",
    cursor="pointer",
    width="100%",
    #box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",  # Adding shadow for better UI
)

active_style = dict(
    **nav_style,
    background_color=rx.color("accent", 8),  # Using Reflex color system
)

def nav_item(text: str, icon: str, message: int=None) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon),
            rx.text(text),
            rx.text(
                rx.cond(message != None, f'{message}', ""),
                margin_left="3rem",
                ),
            spacing="3",
            justify="start",
            width="100%",
        ),
        # color="#330099",
        # background="transparent",
        color=rx.cond(
            pharmercist_state.PharmercistState.current_view == text,
            "gray.200", 
            "#330099"
        ),
        background=rx.cond(
            pharmercist_state.PharmercistState.current_view == text,
            "rgba(51, 0, 153, 1)",
            "transparent"
        ),
        on_click=pharmercist_state.PharmercistState.change_pharm_view(text),
        style=nav_style,
        _hover={
            "background": "rgba(51, 0, 153, 0.8)",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s ease-in-out",
            "color": "#ffffff"
        },
        _active={
            "transform": "scale(0.98)",
            "transition": "all 0.1s ease-in-out"
        },
    )



def sign_out_nav(text: str, icon: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon),
            rx.text(text),
            spacing="3",
            justify="start",
            width="100%",
        ),
        color="#330099",
        background="transparent",
        on_click=pharmercist_state.PharmercistState.logout(),
        style=nav_style,
        _hover={
            "background": "rgba(255, 255, 255, 0.05)",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s ease-in-out"
        },
        _active={
            "transform": "scale(0.98)",
            "transition": "all 0.1s ease-in-out"
        },
    )


def pharm_navbar():
    return rx.box(
        rx.vstack(
            # Navigation items group
            rx.image(src="/school_logo.png", width="45%", margin_bottom="3rem"),
            rx.vstack(
                nav_item("Dashboard", "home"),
                nav_item("Manage Drugs", "pill"),
                nav_item("Prescription", "pill_bottle"),
                sign_out_nav("Logout", "log_out"),
                spacing="0",
                width="100%",
            ),
            # Footer group
            rx.spacer(),  # This pushes the footer to the bottom
            rx.box(
                rx.text(
                    "© 2024 - 2025, Quoin-lab Technology",
                    color="#330099",
                    font_size="12px",
                ),
                padding="1em",
                width="100%",
                text_align="center",
            ),
            height="100%",  # Take full height
            width="100%",
            spacing="0",
            align="center",
        ),
        position="fixed",
        height="100vh",
        width="250px",
        left="0",
        top="0",
        padding_top="4em",
        background_color="#ffffff",
    )
