import reflex as rx
from ..states import student_complaint_state

def card_page():
    return rx.flex(
        rx.box(
            clinic_card(),
            height="77vh",
            overflow="auto",
            width="100%",
            max_width="900px",  # Optional, to limit how wide the scrollable area gets
            align="center",
            justify="center",
            padding="0",
            style={
                # Hide scrollbar background for Webkit browsers (Chrome, Safari, Edge)
                "&::-webkit-scrollbar": {
                    "background": "transparent"
                },
                # Optional: For Firefox
                "scrollbar_width": "thin",
                "scrollbar_color": "transparent transparent",
            }
        ),
        justify="center",    # Center horizontally
        width="100%",
        padding="2rem",
        padding_top="0"
    )

def clinic_card():
    return rx.box(
        rx.vstack(
            # Header Section
            rx.hstack(
                rx.heading("University Clinic Card", size="5", color="#fff"),
                rx.spacer(),
                rx.badge(
                    student_complaint_state.StudentComplaintState.card_data.get("status", "active"),
                    # color_scheme=rx.cond(student_complaint_state.StudentComplaintState.card_data.get("status") == "active", "green", "red"),
                    color_scheme="green",
                    variant="solid"
                ),
                width="100%",
                padding_x="1.5rem",
                padding_top="1rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#eee", opacity=0.8),

            # Avatar and Details
            rx.hstack(
                rx.avatar(
                    src=student_complaint_state.StudentComplaintState.picture,
                    size="6",
                    border="3px solid #fff",
                    box_shadow="xl",
                ),
                rx.vstack(
                    rx.heading(f"{student_complaint_state.StudentComplaintState.student_info["surname"]} {student_complaint_state.StudentComplaintState.student_info["first_name"]}", size="4", color="#fff"),
                    rx.text(f"{student_complaint_state.StudentComplaintState.student_info["matriculation_number"]}", color="#d1d5db", font_size="1em"),
                    rx.text(
                        f"{student_complaint_state.StudentComplaintState.student_info["department_name"]} • {student_complaint_state.StudentComplaintState.student_info["faculty_name"]}",
                        color="#d1d5db", font_size="0.95em"
                    ),
                    align_items="start",
                    spacing="1",
                ),
                spacing="4",
                padding_x="1.5rem",
                padding_bottom=".5rem",
            ),

            # Card Details and QR
            rx.hstack(
                rx.vstack(
                    rx.text("Clinic Number", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(student_complaint_state.StudentComplaintState.clinic_number, color="#fff", font_size="1.1em", margin_bottom="0.5em"),
                    rx.text("Issued", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(student_complaint_state.StudentComplaintState.issue_date, color="#fff", font_size="1.1em", margin_bottom="0.5em"),
                    rx.text("Expires", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(student_complaint_state.StudentComplaintState.expiry_date, color="#fff", font_size="1.1em"),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.image(
                    src=student_complaint_state.StudentComplaintState.student_data.get('qr_code', "N/A"),
                    width="90px",
                    height="90px",
                    border="2px solid #fff",
                    border_radius="md",
                    box_shadow="md",
                ),
                width="100%",
                padding_x="1.5rem",
                padding_bottom=".5rem",
            ),

            rx.divider(margin_y="0.5rem", border_color="#eee", opacity=0.8),

            # Medical Information
            rx.grid(
                rx.box(
                    rx.text("Blood Group", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(
                        rx.cond(
                            student_complaint_state.StudentComplaintState.student_health == None,
                            "N/A",
                            student_complaint_state.StudentComplaintState.student_health.get("blood_group", "N/A")
                            
                            ), 
                        color="#fff"
                        ),
                ),
                rx.box(
                    rx.text("Allergies", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(
                        rx.cond(
                            student_complaint_state.StudentComplaintState.student_health == None,
                            "N/A",
                            student_complaint_state.StudentComplaintState.student_health.get("notes", "None")
                            
                        ),
                        color="#fff"),
                ),
                rx.box(
                    rx.text("Emergency Contact", color="#c7d2fe", font_weight="bold", font_size="0.93em"),
                    rx.text(student_complaint_state.StudentComplaintState.student_data.get("emergency_contact", "N/A"), color="#fff"),
                ),
                columns="3",
                spacing="3",
                width="100%",
                padding_x="1.5rem",
                padding_bottom="1rem",
                
            ),

            # Action Buttons
            
            background="linear-gradient(135deg, #6366f1 0%, #a5b4fc 100%)",
            border_radius="25px",
            box_shadow="2px",
            width="100%",
            max_width="850px",
            spacing="2",
            # justify="center",
            # align="center",
            padding="2rem",
        ),

        rx.hstack(
            # rx.button(
            #     "Print Card",
            #     left_icon="print",
            #     color_scheme="blue",
            #     variant="solid",
            #     border_radius="md",
            # ),
            rx.button(
                "Download PDF",
                left_icon="download",
                variant="outline",
                border_color="blue.500",
                border_radius="md",
            ),
            spacing="3",
            justify="center",
            width="100%",
            margin_top="1rem",
        ),

        width="100%",
        align="center",
        justify="center",
        # max_width="500px",
    )