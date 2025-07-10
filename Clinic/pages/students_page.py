import reflex as rx

from ..components import student_side_bar
from ..pages import digital_card, student_dashboard, student_complaints
from ..states import auth_state, student_state, auth_student

def navbar():
    return rx.box(
        rx.hstack(
            rx.heading(f"University Of Ilorin Clinic", font_size="18px", color="white", text_align="center"),
            justify="center",  
            align="center",  
            width="100%",
            background_color="#330099",
            border_radius="30px",
            padding=".5rem"
        ),

        align="center",
        padding="1rem",
        padding_x="2rem",
        width="100%",
    )


def student_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    student_side_bar.student_navbar(),
                    width="240px",
                    height="100vh",
                    position="fixed",
                    spacing="4",
                    top="0",
                    bg="orange",
                    left="0",
                ),
                rx.box(
                    navbar(),
                    rx.hstack(
                        
                        rx.hstack(
                            rx.image(
                                src="/user_pics.png",
                                width="40px",
                            ),
                            rx.vstack(
                                rx.text(f"{auth_student.UserAuthState.student_data["surname"]} {auth_student.UserAuthState.student_data["first_name"]}", font_size="14px", color="#030f58", text_align="right"),
                                rx.text(f"{auth_student.UserAuthState.student_data["matriculation_number"]}", font_size="12px", color="#666666", text_align="right"),

                                spacing="0",
                            ),
                            spacing="4",
                            align="end",
                        ),
                           
                        
                        rx.hstack(
                            rx.text(f"Today {auth_student.UserAuthState.current_date}", font_size="14px"),
                            color="#333300",
                            align="center",
                        ),
                        
                        border_bottom="2px solid rgba(51, 51, 0, 0.1)",
                        justify="between",
                        align="center",
                        padding="1rem",
                        padding_y="0.5rem",
                        width="100%",
                        box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 4px",
                    ),
                    rx.vstack(
                        rx.match(
                            student_state.StudentState.current_view,
                            ("Dashboard", student_dashboard.dashboard_page()),
                            ("Digital Card", digital_card.card_page()),
                            ("Complaints", student_complaints.complaints_page()),
                            (student_dashboard.dashboard_page()),  # 
                        ),
                        
                        align="center",
                        spacing="4",
                        padding="1rem",
                        min_width="850px",
                    ),
                    padding_left="250px",
                    # margin_top="70px",
                    width="100%",
                    min_height="100vh",
                    min_width="850px",
                    flex="1",
                    background_color="#e6e6e6",
                    align_items="center",
                    justify_content="center",
                ),
                width="100%",
            ),
            width="100%",
            min_height="100vh",
            spacing="0",
        ),
        confirm_logout(),
        # thrift_details(),
        width="100vw",
        height="100vh",
        overflow="hidden",
        background_color="#ffffff",
        min_width="850px",
    )


def confirm_logout():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Are you sure to logout?", color="#333300", text_align="center", margin_y="2rem"),
            rx.hstack(
                rx.button(
                    "Confirm",
                    bg="#A60414",
                    color="white",
                    _hover={"bg": "#4a0309"},
                    on_click=student_state.StudentState.confirm_logout,
                ),

                rx.button(
                    "Cancel",
                    bg="#330099",
                    color="white",
                    _hover={"bg": "#300261"},
                    on_click=student_state.StudentState.cancel_logout,
                ),
                justify="center",
                align="center",
                spacing="3",
            ),
            
            padding="2rem",
            bg="#ffffff",
        ),
        open=student_state.StudentState.is_logout,
    )
