import reflex as rx
from ..states import lab_attendance_state


def test_page():
    return rx.center(
        rx.vstack(
            # Header section with search and create button
            rx.hstack(
                create_record_dialog(),
                rx.hstack(
                    rx.input(
                        placeholder="Search by name or matric...",
                        width="250px",
                        color_scheme="purple",
                        variant="classic",
                        value=lab_attendance_state.LabAttendanceState.search_query,
                        on_change=lab_attendance_state.LabAttendanceState.set_search_query,
                        on_key_down=lab_attendance_state.LabAttendanceState.handle_key_down,
                    ),
                    rx.button(
                        rx.icon("search"),
                        color_scheme="purple",
                        variant="solid",
                        on_click=lab_attendance_state.LabAttendanceState.search_records,
                        border_radius="0 8px 8px 0",
                    ),
                    spacing="0",
                ),
                justify="between",
                width="100%",
                padding_y="2",
            ),

            # Health Records Table
            rx.box(
                rx.cond(
                    lab_attendance_state.LabAttendanceState.health_records,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Student Name"),
                                rx.table.column_header_cell("Matric No"),
                                rx.table.column_header_cell("Department"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="white",
                        ),
                        rx.table.body(
                            rx.foreach(
                                lab_attendance_state.LabAttendanceState.paginated_records,
                                lambda record, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(record["student_name"]),
                                    rx.table.cell(record["matric_number"]),
                                    rx.table.cell(record["department"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=lab_attendance_state.LabAttendanceState.open_dialog(record),
                                            ),
                                            rx.button(
                                                rx.icon("eye", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=lab_attendance_state.LabAttendanceState.view_record(record),
                                            ),
                                            spacing="3",
                                        )
                                    ),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",
                                            "#ffffff",
                                        ),
                                        "color": "#333",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                )
                            )
                        ),
                        variant="surface",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("user", size=32),
                            rx.text("No health records found", size="4"),
                            rx.text("Add a new record to get started", color="gray"),
                            spacing="2",
                            align="center",
                        ),
                        height="300px",
                    )
                ),
                width="100%",
                border_radius="md",
                overflow="hidden",
            ),

            # Pagination Controls
            rx.hstack(
                rx.select(
                    ["5", "10", "15"],
                    value=str(lab_attendance_state.LabAttendanceState.items_per_page),
                    on_change=lab_attendance_state.LabAttendanceState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=lab_attendance_state.LabAttendanceState.prev_page,
                        variant="ghost",
                        disabled=lab_attendance_state.LabAttendanceState.current_page == 1,
                    ),
                    rx.text(
                        f"Page {lab_attendance_state.LabAttendanceState.current_page} of {lab_attendance_state.LabAttendanceState.total_pages}", 
                        color="#330099"
                    ),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=lab_attendance_state.LabAttendanceState.next_page,
                        variant="ghost",
                        disabled=lab_attendance_state.LabAttendanceState.current_page >= lab_attendance_state.LabAttendanceState.total_pages,
                    ),
                    spacing="2",
                ),
                justify="between",
                width="100%",
                padding_top="4",
            ),
            spacing="4",
            width="100%",
            padding="4",
        ),

        view_record_dialog(),  # Add this line
        width="100%",
        on_mount=lab_attendance_state.LabAttendanceState.load_health_records,
    )


def create_record_dialog():
    """Dialog for creating/editing health records."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("Add New Record"),
                    spacing="2",
                ),
                on_click=lab_attendance_state.LabAttendanceState.open_dialog(None),
                color="white",
                bg="linear-gradient(45deg, #330099, #4d4dff)",
                _hover={
                    "transform": "translateY(-2px)",
                    "transition": "all 0.2s ease-in-out"
                },
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    lab_attendance_state.LabAttendanceState.is_editing,
                    "Edit Health Record",
                    "Create New Health Record"
                )
            ),
            rx.dialog.description(
                "Fill in the student's health details",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Matric Number",
                    width="100%",
                    value=lab_attendance_state.LabAttendanceState.matric_number,
                    on_change=lab_attendance_state.LabAttendanceState.set_matric_number,
                    is_disabled=lab_attendance_state.LabAttendanceState.is_editing,
                ),
                rx.select(
                    ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                    placeholder="Blood Group",
                    value=lab_attendance_state.LabAttendanceState.blood_group,
                    on_change=lab_attendance_state.LabAttendanceState.set_blood_group,
                ),
                rx.select(
                    ["AA", "AS", "SS", "AC", "SC"],
                    placeholder="Genotype",
                    value=lab_attendance_state.LabAttendanceState.genotype,
                    on_change=lab_attendance_state.LabAttendanceState.set_genotype,
                ),
                rx.input(
                    placeholder="Height (cm)",
                    type="number",
                    width="100%",
                    value=lab_attendance_state.LabAttendanceState.height,
                    on_change=lab_attendance_state.LabAttendanceState.set_height,
                ),
                rx.input(
                    placeholder="Weight (kg)",
                    type="number",
                    width="100%",
                    value=lab_attendance_state.LabAttendanceState.weight,
                    on_change=lab_attendance_state.LabAttendanceState.set_weight,
                ),
                rx.input(
                    placeholder="Test Date (YYYY-MM-DD)",
                    width="100%",
                    value=lab_attendance_state.LabAttendanceState.test_date,
                    on_change=lab_attendance_state.LabAttendanceState.set_test_date,
                ),
                rx.text_area(
                    placeholder="Additional Notes",
                    width="100%",
                    value=lab_attendance_state.LabAttendanceState.notes,
                    on_change=lab_attendance_state.LabAttendanceState.set_notes,
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=lab_attendance_state.LabAttendanceState.close_dialog,
                        variant="soft",
                    ),
                    rx.button(
                        rx.cond(
                            lab_attendance_state.LabAttendanceState.is_saving,
                            "Saving...",
                            rx.cond(
                                lab_attendance_state.LabAttendanceState.is_editing,
                                "Update Record",
                                "Create Record"
                            ),
                        ),
                        on_click=lab_attendance_state.LabAttendanceState.submit_record,
                        color_scheme="purple",
                    ),
                    spacing="3",
                    margin_top="1em",
                ),
                spacing="3",
            ),
            width="90vw",
            max_width="450px",
        ),
        open=lab_attendance_state.LabAttendanceState.show_dialog,
    )

def view_record_dialog():
    """Dialog to view complete health record details"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Student Health Record"),
            rx.dialog.description(
                "Complete health information",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.hstack(
                    # Student Information Column
                    rx.vstack(
                        rx.heading("Student Information", size="4"),
                        rx.hstack(
                            rx.text("Name:", width="120px", font_weight="bold"),
                            rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("student_name", "")),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Matric No:", width="120px", font_weight="bold"),
                            rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("matric_number", "")),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Department:", width="120px", font_weight="bold"),
                            rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("department", "")),
                            width="100%"
                        ),
                        spacing="2",
                        width="50%",
                        padding_right="2"
                    ),
                    # Medical Information Column
                    rx.vstack(
                        rx.heading("Medical Information", size="4"),
                        rx.hstack(
                            rx.text("Blood Group:", width="120px", font_weight="bold"),
                            rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("blood_group", "Not specified")),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Genotype:", width="120px", font_weight="bold"),
                            rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("genotype", "Not specified")),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Height:", width="120px", font_weight="bold"),
                            rx.text(f"{lab_attendance_state.LabAttendanceState.selected_record.get('height', '')} cm"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Weight:", width="120px", font_weight="bold"),
                            rx.text(f"{lab_attendance_state.LabAttendanceState.selected_record.get('weight', '')} kg"),
                            width="100%"
                        ),
                        spacing="2",
                        width="50%",
                        padding_left="2"
                    ),
                    width="100%"
                ),
                rx.divider(),
                rx.vstack(
                    rx.heading("Test Details", size="4"),
                    rx.hstack(
                        rx.text("Test Date:", width="120px", font_weight="bold"),
                        rx.text(lab_attendance_state.LabAttendanceState.selected_record.get("test_date", "")),
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Notes:", width="120px", font_weight="bold"),
                        rx.text(
                            lab_attendance_state.LabAttendanceState.selected_record.get("notes", "No additional notes"),
                            width="100%"
                        ),
                        width="100%"
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button(
                    "Close",
                    on_click=lab_attendance_state.LabAttendanceState.set_show_view_dialog(False),
                    color_scheme="purple",
                    margin_top="1em",
                    width="100%"
                ),
                spacing="4",
                width="100%",
            ),
            width="90vw",
            max_width="600px",
        ),
        open=lab_attendance_state.LabAttendanceState.show_view_dialog,
    )