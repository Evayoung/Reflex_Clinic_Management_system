import reflex as rx
from ..states import student_complaint_state


def complaints_page():
    return rx.center(
        rx.vstack(
            rx.hstack(
                create_complaint_dialog(),
                justify="between",
                width="100%",
                padding_y="2",
            ),

            visit_detail_dialog(),
            rx.box(
                rx.cond(
                    student_complaint_state.StudentComplaintState.visits,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Visit Date"),
                                rx.table.column_header_cell("Doctor"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Action"),
                            ),
                            background_color="#330099",
                            color="white",
                        ),
                        rx.table.body(
                            rx.foreach(
                                student_complaint_state.StudentComplaintState.visits,
                                lambda visit, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(visit["visit_date"]),
                                    rx.table.cell(visit["doctor_name"]),
                                    rx.table.cell(visit["status"]),
                                    rx.table.cell(
                                        rx.button(
                                            "View",
                                            variant="soft",
                                            size="2",
                                            on_click=lambda v_id=visit["visit_id"]: student_complaint_state.StudentComplaintState.view_visit(v_id)
                                        )

                                    ),
                                    style={
                                        "background_color": rx.cond(idx % 2 == 0, "#f8f8ff", "#ffffff"),
                                        "font_size": "14px",
                                        "color": "#2B2B4E",
                                        # "padding": "10px"
                                    }
                                )
                            )
                        ),
                        variant="surface",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("activity", size=32),
                            rx.text("No visits found", size="4"),
                            rx.text("Click 'New Complaint' to start a visit.", color="gray"),
                            spacing="2",
                            align="center",
                        ),
                        height="300px"
                    )
                ),
                width="100%",
                border_radius="md",
                overflow="hidden",
            ),

            spacing="4",
            width="100%",
            padding="4",
        ),
        # on_mount=student_complaint_state.StudentComplaintState.on_mount,
        width="100%"
    )


def create_complaint_dialog():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("New Complaint"),
                    spacing="2",
                ),
                on_click=student_complaint_state.StudentComplaintState.open_dialog,
                color="white",
                bg="linear-gradient(45deg, #006600, #00cc66)",
                _hover={
                    "transform": "translateY(-2px)",
                    "transition": "all 0.2s ease-in-out"
                },
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("New Clinic Complaint"),
            rx.dialog.description("Select a doctor schedule and enter your complaint"),
            rx.vstack(
                rx.select(
                    student_complaint_state.StudentComplaintState.schedule_options,
                    value=student_complaint_state.StudentComplaintState.selected_schedule_str,
                    on_change=student_complaint_state.StudentComplaintState.set_selected_schedule,
                    placeholder="Choose available schedule",
                ),
                rx.text_area(
                    placeholder="e.g., I've been having migraines...",
                    value=student_complaint_state.StudentComplaintState.complaint_description,
                    on_change=student_complaint_state.StudentComplaintState.set_complaint_description,
                    width="100%",
                    rows="5",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=student_complaint_state.StudentComplaintState.close_dialog,
                        variant="soft"
                    ),
                    rx.button(
                        rx.cond(
                            student_complaint_state.StudentComplaintState.is_sumbmit,
                            rx.spinner(size="3", color="white"),
                            rx.text("Submit Complaint", color="white")
                        ),
                        on_click=student_complaint_state.StudentComplaintState.submit_complaint,
                        disabled=student_complaint_state.StudentComplaintState.is_sumbmit,
                        color_scheme="purple"
                    ),
                    spacing="3",
                    margin_top="1em"
                ),
                spacing="3"
            ),
            width="90vw",
            max_width="450px"
        ),
        open=student_complaint_state.StudentComplaintState.show_dialog
    )


def visit_detail_dialog():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Visit Details"),
            rx.dialog.description(
                "See the complaint, diagnosis, and prescriptions for this visit.",
                size="2",
                margin_bottom="10px",
            ),
            rx.vstack(
                # Visit Metadata
                rx.flex(
                    rx.text(f"Doctor: {student_complaint_state.StudentComplaintState.selected_visit['doctor_name']}", weight="bold", font_size="14px"),
                    rx.text(f"Date: {student_complaint_state.StudentComplaintState.selected_visit['visit_date']}", font_size="14px"),
                    rx.badge(f"Status: {student_complaint_state.StudentComplaintState.selected_visit['status']}", size="3", color_scheme=rx.cond(student_complaint_state.StudentComplaintState.selected_visit['status'] == "Completed", "green", "red")),
                    spacing="4",
                    margin_bottom="8px",
                ),
                rx.divider(),

                # Complaint
                rx.vstack(
                    rx.heading("Complaint", size="3", margin_top="4px"),
                    rx.text(
                        student_complaint_state.StudentComplaintState.student_compalints["description"],
                        margin_bottom="8px", 
                        font_size="14px"
                    ),
                    width="100%",
                    spacing="2",
                ),

                # Diagnosis
                rx.cond(
                    student_complaint_state.StudentComplaintState.diagnosis,
                    rx.vstack(
                        rx.heading("Diagnosis", size="3", margin_top="4px"),
                        rx.text(
                            student_complaint_state.StudentComplaintState.diagnosis["diagnosis_description"],
                            color="teal",
                            font_size="14px",
                            margin_bottom="4px"
                        ),
                        rx.text(
                            f"Treatment: {student_complaint_state.StudentComplaintState.diagnosis['treatment_plan']}",
                            color="teal", 
                            font_size="14px"
                        ),
                        spacing="2",
                    ),
                    rx.text("No diagnosis yet.", color="gray", margin_bottom="4px")
                ),

                # Prescriptions
                rx.cond(
                    student_complaint_state.StudentComplaintState.prescriptions,
                    rx.vstack(
                        rx.heading("Prescriptions", size="3", margin_top="4px"),
                        
                        rx.foreach(
                            student_complaint_state.StudentComplaintState.prescriptions,
                            lambda p: rx.card(
                                rx.vstack(
                                    rx.list.unordered(
                                        rx.text(f"Drug: {p['drug_name']}", color="#BDA0F8", font_size="14px"),
                                        rx.text(f"Dosage: {p['dosage']}", color="#BDA0F8", font_size="14px"),
                                        rx.text(f"Instructions: {p['instructions']}", color="#BDA0F8", font_size="14px"),
                                        spacing="2"
                                    ),
                                )
                            )
                            
                        # )
                        ),
                        spacing="2"
                    ),
                    rx.text("No prescriptions.", color="gray", margin_bottom="4px", font_size="14px")
                ),

                # Close Button
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Close", 
                            variant="soft", 
                            color_scheme="gray",
                            on_click=student_complaint_state.StudentComplaintState.close_visit_detail
                            )
                    ),
                    justify="end",
                    margin_top="16px"
                ),

                spacing="4",
            ),
            max_width="500px",
            padding="24px",
        ),
        open=student_complaint_state.StudentComplaintState.show_visit_detail,
    )
