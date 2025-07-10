import reflex as rx
from ..states import auth_state, admin_state, student_state, student_complaint_state

def dashboard_page():
    return rx.box(
        rx.vstack(
            
            rx.hstack(
                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{student_complaint_state.StudentComplaintState.dashboard_data["total_visits"]}",),
                            rx.text(f"My Visits", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="50%",
                    spacing="4",
                    background_color="#ff6600",
                    border_radius="5px",
                ),

                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{student_complaint_state.StudentComplaintState.dashboard_data["pending_visits"]}",),
                            rx.text(f"Pending Visits", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="50%",
                    spacing="2",
                    background_color="#339966",
                    border_radius="5px",
                ),

                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{student_complaint_state.StudentComplaintState.total_doctors}",),
                            rx.text(f"Doctors Available", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="50%",
                    spacing="2",
                    background_color="#660287",
                    border_radius="5px",
                ),


                width="100%",
                align="center",
                justify="between",
                spacing="6",
            ),
            
            rx.hstack(
                rx.heading("Doctors List", color="grey"),
                align="start",
                padding=".5rem",
                padding_x="2rem",
                width="100%",
            ),
            
            rx.box(
                rx.grid(
                    rx.foreach(
                        student_complaint_state.StudentComplaintState.doctors,
                        lambda doctor: rx.box(
                            rx.hstack(
                                rx.hstack(
                                    rx.image(
                                        src="/user_pics.png",
                                        width="65px",
                                        height="65px",
                                        border_radius="50%",
                                    ),
                                    rx.box(width="5px", height="70px", bg="grey", border_radius="5px"),
                                    rx.vstack(
                                        rx.heading(doctor["name"], color="black", size="4"),
                                        rx.text(doctor["doctor_id"], color="grey", size="3"),
                                        align="start",
                                        spacing="1",
                                    ),
                                    width="100%",
                                    align="center",
                                    height="100%",
                                    spacing="4",
                                ),
                                rx.button(
                                    "View Profile",
                                    on_click=student_complaint_state.StudentComplaintState.open_doctor_dialog(doctor),
                                    size="3",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "transition": "all 0.2s ease-in-out",
                                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                                    },
                                ),
                                padding="1rem",
                                bg="#ffffff",
                                border_radius="10px",
                                width="100%",
                                spacing="4",
                                align="center",
                                justify="between",
                                _hover={
                                    "box_shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px",
                                    "transform": "translateY(-2px)",
                                    "transition": "all 0.2s ease-in-out",
                                },
                            ),
                            width="100%",
                        ),
                    ),
                    
                    columns="2",
                    spacing="4",
                    width="100%",
                    padding="1rem",
                ),
                width="100%",
                min_height="350px",
                overflow="hidden",
            ),
            
            align="center",
            width="100%",
            spacing="3",
            border_radius="10px",
        ),
        
        doctor_dialog(),
        
        border_radius="10px",
        padding="1rem",
        width="100%",
    )


def doctor_card(doctor: dict):
    """Individual doctor card component"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src=doctor["image"],
                    width="65px",
                    height="65px",
                    border_radius="50%",
                ),
                rx.box(width="5px", height="70px", bg="grey", border_radius="5px"),
                rx.vstack(
                    rx.heading(doctor["name"], color="black", size="sm"),
                    rx.text(doctor["specialty"], color="grey", size="xs"),
                    align="start",
                    spacing="1",
                ),
                width="100%",
                align="center",
                height="100%",
                spacing="4",
            ),
            rx.button(
                "View Profile",
                on_click=student_complaint_state.StudentComplaintState.show_doctor_dialog(doctor),
                size="3",
                _hover={
                    "transform": "translateY(-2px)",
                    "transition": "all 0.2s ease-in-out",
                    "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                },
            ),
            padding="1rem",
            bg="#ffffff",
            border_radius="10px",
            width="100%",
            spacing="4",
            align="center",
            justify="between",
            _hover={
                "box_shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px",
                "transform": "translateY(-2px)",
                "transition": "all 0.2s ease-in-out",
            },
        ),
        width="100%",
    )




def doctor_dialog():
    """Dialog component to show doctor details"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Doctor Profile"),
            rx.dialog.description(
                rx.vstack(
                    rx.image(
                        src="/user_pics.png",
                        width="100px",
                        height="100px",
                        border_radius="50%",
                        margin_bottom="1rem",
                    ),
                    rx.heading(student_complaint_state.StudentComplaintState.selected_doctor.get("name", ""), size="4"),
                    rx.text(student_complaint_state.StudentComplaintState.selected_doctor.get("doctor_id", ""), color="gray"),
                    rx.divider(),
                    rx.hstack(
                        rx.text("Contact:", weight="bold"),
                        rx.text(student_complaint_state.StudentComplaintState.selected_doctor.get("email", "")),  # Replace with actual data
                        align="center",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Phone:", weight="bold"),
                        rx.text(student_complaint_state.StudentComplaintState.selected_doctor.get("phone", "")),  # Replace with actual data
                        align="center",
                        spacing="2",
                    ),
                    spacing="3",
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Close",
                    on_click=student_complaint_state.StudentComplaintState.close_doctor_dialog,
                    margin_top="1rem",
                ),
            ),
            width="90vw",
            max_width="500px",
        ),
        open=student_complaint_state.StudentComplaintState.show_doctor_dialog,
        on_open_change=student_complaint_state.StudentComplaintState.set_show_dialog,
    )