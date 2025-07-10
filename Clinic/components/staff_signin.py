import reflex as rx
from ..states.auth_state import UserAuthState


def sign_in():
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Staff Sign In", font_size=".75rem", align="center", color="white"),  
                rx.input(
                    placeholder="User ID", 
                    width="100%", 
                    height="40px",
                    color="white",
                    required=True,
                    value=UserAuthState.username,
                    on_change=UserAuthState.set_username,
                    ),
                rx.input(
                    placeholder="Password", 
                    type="password", 
                    width="100%", 
                    height="40px",
                    color="white",
                    required=True,
                    value=UserAuthState.password,
                    on_change=UserAuthState.set_password,
                    ),
                rx.button(
                    rx.cond(
                        UserAuthState.loading,  
                        rx.spinner(size="2", color="white"), 
                        rx.text("Sign In")  
                    ),
                    bg="#330099", 
                    color="white", 
                    width="70%", 
                    height="45px",
                    _hover={
                        "background": "rgba(51, 0, 153, 0.3)",
                        "transform": "translateY(-2px)",
                        "transition": "all 0.2s ease-in-out"
                    },
                    on_click=UserAuthState.login(),
                    # disabled=LoginFormState.loading,  # Disable button when loading
                ),
                
                rx.hstack(
                    rx.link(
                        "Back to Home",
                        on_click=UserAuthState.change_submain_view("Default"),
                        bg="transparent",
                        p=2,
                        align="center",
                        font_size="12px",
                        color="white",
                        _hover={
                            "color": "rgba(255, 255, 255, 0.5)",
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out"
                        },
                    ),
                ),
                spacing="4",
                width="100%",
                align="center",
            ),
            width="100%",
        ),

        max_width=rx.breakpoints(sm="90%", md="600px"),
        padding=["20px", "40px"],
        min_width="420px",
        min_height="150px",
        shadow="lg",  
        border_radius="lg",  
        bg="rgba(255, 255, 255, 0.05)", 
        backdrop_filter="blur(10px)", 
    )
