import reflex as rx
from ..states import auth_student, auth_state

def sign_up():
    color = "rgb(107,99,246)"
    return rx.card(
        rx.vstack(
            rx.heading("Sign Up", size="5", align="center", color="white"),  # Heading outside the scrollable container
            rx.form(
                rx.box(
                    rx.vstack(
                        rx.input(
                            placeholder="Surname", 
                            type="text",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.surname,
                            on_change=auth_student.UserAuthState.change_surname,
                        ),
                        rx.input(
                            placeholder="First Name", 
                            type="text",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.firstname,
                            on_change=auth_student.UserAuthState.change_firstname,
                        ),
                        rx.input(
                            placeholder="Matriculation Number",
                            type="text",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.matric,
                            on_change=auth_student.UserAuthState.change_matric,
                        ),
                        rx.select(
                            auth_student.UserAuthState.academic_sessions,
                            value=auth_student.UserAuthState.academic_session,
                            on_change=auth_student.UserAuthState.change_session,
                            placeholder="Select Session",
                            width="100%",
                            size="3",
                            margin_bottom="1rem",
                            color="white",
                            bg="white",  # Add background color for better visibility
                            border_color="white",  # Add border color
                            variant="classic",
                            _hover={"border_color": "white"},  # Hover effect
                        ),
                        
                        rx.input(
                            placeholder="Email",
                            type="email",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.email,
                            on_change=auth_student.UserAuthState.change_email,
                        ),
                        rx.input(
                            placeholder="Phone", 
                            type="tel",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.phone,
                            on_change=auth_student.UserAuthState.change_phone,
                        ),
                        rx.input(
                            placeholder="Date of Birth",
                            type="date",
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.dob,
                            on_change=auth_student.UserAuthState.change_dob,
                        ),
                        rx.select(
                            auth_student.UserAuthState.values,
                            value=auth_student.UserAuthState.value,
                            on_change=auth_student.UserAuthState.change_value,
                            placeholder="Select Gender",
                            width="100%",
                            size="3",
                            margin_bottom="1rem",
                            color="white",
                            bg="white",  # Add background color for better visibility
                            border_color="white",  # Add border color
                            variant="classic",
                            _hover={"border_color": "white"},  # Hover effect
                        ),
                        rx.input(
                            placeholder="Address", 
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.address,
                            on_change=auth_student.UserAuthState.change_address,
                        ),
                        rx.select(
                            auth_student.UserAuthState.faculties,
                            value=auth_student.UserAuthState.faculty,
                            on_change=auth_student.UserAuthState.change_faculty,
                            placeholder="Select Faculty",
                            width="100%",
                            size="3",
                            margin_bottom="1rem",
                            color="white",
                            bg="white",  # Add background color for better visibility
                            border_color="white",  # Add border color
                            variant="classic",
                            _hover={"border_color": "white"},  # Hover effect
                        ),
                        rx.select(
                            auth_student.UserAuthState.departments,
                            value=auth_student.UserAuthState.department,
                            on_change=auth_student.UserAuthState.change_department,
                            placeholder="Select Department",
                            width="100%",
                            size="3",
                            margin_bottom="1rem",
                            color="white",
                            bg="white",  # Add background color for better visibility
                            border_color="white",  # Add border color
                            variant="classic",
                            _hover={"border_color": "white"},  # Hover effect
                        ),
                        rx.select(
                            auth_student.UserAuthState.levels,
                            value=auth_student.UserAuthState.level,
                            on_change=auth_student.UserAuthState.change_level,
                            placeholder="Select Level",
                            width="100%",
                            size="3",
                            margin_bottom="1rem",
                            color="white",
                            bg="white",  # Add background color for better visibility
                            border_color="white",  # Add border color
                            variant="classic",
                            _hover={"border_color": "white"},  # Hover effect
                        ),
                        rx.input(
                            placeholder="Emergency Contact", 
                            type="tel", 
                            width="100%", 
                            height="40px",
                            color="white",
                            required=True,
                            value=auth_student.UserAuthState.guidance,
                            on_change=auth_student.UserAuthState.change_guidance,
                        ),

                        rx.vstack(
                            rx.upload(
                                rx.vstack(
                                    rx.button(
                                        "Select Picture",
                                        color=color,
                                        bg="white",
                                        border=f"1px solid {color}",
                                    ),
                                    # rx.text("Drag and drop a picture here or click to select"),
                                ),
                                id="upload_passport",
                                max_files=1,  # Only allow one file
                                accept={
                                    "image/png": [".png"],
                                    "image/jpeg": [".jpg", ".jpeg"],
                                    "image/gif": [".gif"],
                                    "image/webp": [".webp"],
                                },
                                border=f"1px dotted {color}",
                                padding="1rem",
                                on_drop=auth_student.UserAuthState.handle_upload(rx.upload_files(upload_id="upload_passport")),
                            ),
                            rx.text(rx.selected_files("upload_passport")),
                            padding="0",
                        ),
                        rx.button(
                            rx.cond(
                                auth_student.UserAuthState.submit,
                                "Processing...",
                                "Sign Up"
                            ),
                            type="submit",
                            bg="#330099", 
                            color="white", 
                            width="70%", 
                            height="45px",
                            _hover={
                                "background": "rgba(51, 0, 153, 0.3)",
                                "transform": "translateY(-2px)",
                                "transition": "all 0.2s ease-in-out"
                            },
                            on_click=auth_student.UserAuthState.create_account,
                            disabled=auth_student.UserAuthState.submit,
                        ),
                        rx.hstack(
                            rx.link(
                                "Sign In Instead?",
                                on_click=auth_state.UserAuthState.change_submain_view("Student"),
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
                    height="400px",  
                    overflow_y="scroll", 
                    width="100%",
                    style={
                            # Hide scrollbar background for Webkit browsers (Chrome, Safari, Edge)
                            "&::-webkit-scrollbar": {
                                "background": "transparent"
                            },
                            # Optional: For Firefox
                            "scrollbar_width": "thin",
                            "scrollbar_color": "black transparent",
                        }
                ),
                width="100%",
            ),
            spacing="4",  
            align="center",
        ),
        max_width=rx.breakpoints(sm="90%", md="600px"),  
        padding=["20px", "40px"],  
        min_width="420px",
        min_height="150px",
        shadow="lg",  
        border_radius="lg",  
        bg="rgba(255, 255, 255, 0.05)", 
        backdrop_filter="blur(10px)", 
        on_mount=auth_student.UserAuthState.call_fetch_preliminary
    )