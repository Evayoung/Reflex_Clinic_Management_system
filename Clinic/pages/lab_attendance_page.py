import reflex as rx

from . import admin_student
from ..components import footer, lab_side_bar
from ..pages import lab_dashboard, lab_test
from ..states import auth_state, lab_attendance_state

def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text(f"Welcome, {auth_state.UserAuthState.username.split(" ")[0]}", font_size="18px", color="white", text_align="left")
            ),
            rx.hstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(f"{auth_state.UserAuthState.username}", font_size="14px", color="#A1C7DE", text_align="right"),
                        rx.text(f"{auth_state.UserAuthState.user_id}", font_size="12px", color="#6788B8", text_align="right"),

                        spacing="0",
                    ),
                    rx.image(
                        src="/user_pics.png",
                        width="40px",
                    ),
                    
                    spacing="4",
                    align="end",
                ),
                # bg="orange",
                width="250px",
                justify="end",
            ),

            justify="between",  
            align="center",  
            width="100%",
        ),
        justify="between",
        align="center",
        padding="1rem",
        width="100%",
        
        background_color="#330099",
    )



def lab_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    lab_side_bar.lab_navbar(),
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
                            rx.text(f"{lab_attendance_state.LabAttendanceState.navigator} /", font_size="14px"),
                            color="#333300",
                            align="center",
                            margin_right="2rem",
                            width="300px",
                        ),
                        
                        
                        rx.hstack(
                            rx.text(f"Today {auth_state.UserAuthState.current_date}", font_size="14px"),
                            color="#333300",
                            align="center",
                            
                        ),
                        rx.hstack(
                            rx.text(f"Current User: {auth_state.UserAuthState.role}", font_size="14px"),
                            color="#333300",
                            align="center",
                            cursor="pointer",
                            # on_click=DashboardState.show_group_details,
                            _hover={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "transform": "translateY(-2px)",
                                "transition": "all 0.2s ease-in-out"
                            }
                        ),
                        
                        border_bottom="2px solid rgba(51, 51, 0, 0.1)",
                        justify="between",
                        align="center",
                        padding="1rem",
                        padding_y="0.7rem",
                        width="100%",
                        box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 4px",
                    ),
                    rx.vstack(
                        rx.match(
                            lab_attendance_state.LabAttendanceState.current_view,
                            ("Dashboard", lab_dashboard.dashboard_page()),
                            ("Medical Test", lab_test.test_page()),
                            (lab_dashboard.dashboard_page()),  # 
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
                    on_click=lab_attendance_state.LabAttendanceState.confirm_logout,
                ),

                rx.button(
                    "Cancel",
                    bg="#330099",
                    color="white",
                    _hover={"bg": "#300261"},
                    on_click=lab_attendance_state.LabAttendanceState.cancel_logout,
                ),
                justify="center",
                align="center",
                spacing="3",
            ),
            
            padding="2rem",
            bg="#ffffff",
        ),
        open=lab_attendance_state.LabAttendanceState.is_logout,
    )
