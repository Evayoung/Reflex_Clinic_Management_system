import reflex as rx
from ..states import auth_state

def dashboard_page():
    return rx.center(
        rx.vstack(
            
            rx.vstack(
                rx.image(
                    src="/user_pics.png",
                    width="90px",
                    height="auto",
                    border_radius="8px",
                ),

                rx.vstack(
                    rx.heading(f"{auth_state.UserAuthState.username}", size="6", color="#0E31FA", margin_bottom="1rem"),
                    rx.text(f"{auth_state.UserAuthState.user_id}", color="#13268F", font_size="16px"),
                    rx.text(f"{auth_state.UserAuthState.phone}", color="#13268F", font_size="16px"),
                    rx.text(f"{auth_state.UserAuthState.email}", color="#13268F", font_size="16px"),
                    spacing="1",
                    align="center",
                    justify="center",
                    width="100%",
                ),
                align="center",
                justify="center",
                padding="2rem",
                width="100%",
            ),
            
            
            align="center",
            width="100%",
            spacing="5",
            border_radius="10px",
        ),
        
        border_radius="10px",
        padding="1rem",
        width="100%",
        # on_mount=admin_state.AdminState.on_mount,
    )

