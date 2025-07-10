import reflex as rx
from ..states import auth_state, admin_state, doctor_availability_state

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

            rx.hstack(
                rx.hstack(
                    rx.heading(f"{doctor_availability_state.DoctorAvailabilityState.appointment_lists}", size="6", color="#FFFFFF"),
                    rx.text(f"Pending Schedules", font_size="16px", color="#FFFFFF"),
                    rx.icon("circle-arrow-right", size=16), 
                    width="25%",
                    padding=".75rem",
                    align="center",
                    justify="center",
                    bg="#FF6600",
                    spacing="2",
                    cursor="pointer",
                    border_radius="25px",
                    _hover={
                        "transform": "translateY(-2px)",
                        "transition": "all 0.2s ease-in-out",
                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                    },
                ),

                rx.hstack(
                    rx.heading(f"{doctor_availability_state.DoctorAvailabilityState.total_visits}", size="6", color="#FFFFFF"),
                    rx.text(f"Total Visits Recieved", font_size="16px", color="#FFFFFF"),
                    rx.icon("circle-arrow-right", size=16), 
                    width="25%",
                    padding=".75rem",
                    align="center",
                    justify="center",
                    bg="#339966",
                    cursor="pointer",
                    spacing="2",
                    border_radius="25px",
                    _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                ),
                width="100%",
                padding="2rem",
                align="center",
                justify="center",
                spacing="5",
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

