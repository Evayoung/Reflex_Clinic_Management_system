import reflex as rx
from ..states import auth_student, auth_state
def sign_in():
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Student Sign In", size="5", align="center", color="white"),  # Responsive font size
                rx.input(
                    placeholder="Matriculation Number", 
                    width="100%", 
                    height="40px",
                    color="white",
                    required=True,
                    value=auth_student.UserAuthState.matric_number,
                    on_change=auth_student.UserAuthState.change_matric_number,
                    ),
                rx.input(
                    placeholder="Password", 
                    type="password", 
                    width="100%", 
                    height="40px",
                    color="white",
                    required=True,
                    value=auth_student.UserAuthState.password,
                    on_change=auth_student.UserAuthState.change_password,
                    ),
                rx.button(
                    rx.cond(
                        auth_student.UserAuthState.loading,  
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
                    on_click=auth_student.UserAuthState.login,
                    disabled=auth_student.UserAuthState.loading,
                ),

                rx.vstack(
                    rx.link(
                        "SignUp",
                        on_click=auth_state.UserAuthState.change_submain_view("Create Student"),
                        bg="transparent",
                        p=2,
                        text_align="center",
                        font_size="12px",
                        color="white",
                        _hover={
                            "color": "rgba(255, 255, 255, 0.5)",
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out"
                        },
                    ),

                    rx.link(
                        "Back to Home",
                        on_click=auth_state.UserAuthState.change_submain_view("Default"),
                        bg="transparent",
                        p=2,
                        text_align="center",
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

        max_width=rx.breakpoints(sm="90%", md="600px"),  # Responsive width: 90% on mobile, 500px on desktop
        padding=["20px", "40px"],  # Responsive padding: smaller on mobile, larger on desktop
        min_width="420px",
        min_height="150px",
        shadow="lg",  
        border_radius="lg",  
        bg="rgba(255, 255, 255, 0.05)", 
        backdrop_filter="blur(10px)", 
    )
