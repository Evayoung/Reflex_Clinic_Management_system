import reflex as rx
from ..states import dispensation_state

def dispensation_page():
    return rx.box(
        rx.vstack(
            # Error Message
            rx.cond(
                dispensation_state.DispensationState.error_message,
                rx.text(dispensation_state.DispensationState.error_message, color="red", size="4"),
            ),
            # Header section with search bar
            rx.hstack(
                rx.input(
                    placeholder="Enter student matriculation number...",
                    width="400px",
                    color_scheme="purple",
                    variant="classic",
                    value=dispensation_state.DispensationState.search_query,
                    on_change=dispensation_state.DispensationState.set_search_query,
                ),
                rx.button(
                    rx.cond(
                        dispensation_state.DispensationState.is_loading,
                        rx.spinner(size="2"),
                        rx.icon("search")
                    ),
                    color_scheme="purple",
                    variant="solid",
                    border_radius="0 8px 8px 0",
                    on_click=dispensation_state.DispensationState.search_student,
                ),
                spacing="0",
            ),
            # Student Details Section
            rx.cond(
                dispensation_state.DispensationState.student,
                rx.vstack(
                    rx.card(
                        rx.hstack(
                            rx.vstack(
                                rx.text(f"Full Name: {dispensation_state.DispensationState.student_full_name}", font_weight="bold", font_size="14px", color="#330099"),
                                rx.text(f"Matric No.: {dispensation_state.DispensationState.matriculation_number}", font_size="14px", color="grey"),
                                rx.text(f"Date Of Birth: {dispensation_state.DispensationState.date_of_birth}", font_size="14px", color="grey"),
                                rx.text(f"Gender: {dispensation_state.DispensationState.gender}", font_size="14px", color="grey"),
                                rx.text(f"Emergency Contact: {dispensation_state.DispensationState.emergency_contact}", font_size="14px", color="grey"),
                                spacing="2",
                                width="48%",
                            ),
                            rx.vstack(
                                rx.text(f"Email Address: {dispensation_state.DispensationState.email}", font_size="14px", color="grey"),
                                rx.text(f"Phone No.: {dispensation_state.DispensationState.phone}", font_size="14px", color="grey"),
                                rx.text(f"Department: {dispensation_state.DispensationState.department_name}", font_size="14px", color="grey"),
                                rx.text(f"Faculty: {dispensation_state.DispensationState.faculty_name}", font_size="14px", color="grey"),
                                rx.text(f"Department: {dispensation_state.DispensationState.level_name}", font_size="14px", color="grey"),
                                spacing="2",
                                width="48%",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        width="100%",
                        border_radius="md",
                        padding="1rem",
                        padding_x="4rem",
                        background_color="#f0f0f0",
                    ),
                width="100%",
                padding_x="2rem",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("search", size=32, color="grey"),
                        rx.text("No student found", size="3", color="grey"),
                        rx.text("Enter a valid matriculation number to search", color="gray"),
                        spacing="1",
                        align="center",
                    ),
                    # height="200px",
                    width="100%"
                )
            ),
            # Prescription Table Section
            rx.cond(
                dispensation_state.DispensationState.prescriptions,
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Visit Date"),
                                rx.table.column_header_cell("Drug"),
                                rx.table.column_header_cell("Dosage"),
                                rx.table.column_header_cell("Instructions"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#ffffff",
                        ),
                        rx.table.body(
                            rx.foreach(
                                dispensation_state.DispensationState.prescriptions,
                                lambda prescription, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(prescription.get('visit_date', '')),
                                    rx.table.cell(prescription.get('drug_name', '')),
                                    rx.table.cell(prescription.get('dosage', '')),
                                    rx.table.cell(prescription.get('instructions', '')),
                                    rx.table.cell(
                                        rx.button(
                                            "Dispense",
                                            color_scheme="green",
                                            variant="solid",
                                            size="2",
                                            on_click=lambda p=prescription: dispensation_state.DispensationState.open_dispense_modal(p['prescription_id']),
                                        )
                                    ),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",
                                            "#ffffff",
                                        ),
                                        "color": "#333300",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                )
                            )
                        ),
                        variant="surface",
                    ),
                    width="100%",
                    border_radius="md",
                    overflow="hidden",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("clipboard", size=32, color="grey"),
                        rx.text("No prescriptions found", size="3", color="grey"),
                        rx.text("Ensure the student has a prescription", color="gray"),
                        spacing="1",
                        align="center",
                        width="100%",
                    ),
                    # height="200px",
                    width="100%",
                )
            ),
            # Dispensation Modal
            create_dispense_modal(),
            # Dispensed Drugs Table Section
            rx.cond(
                dispensation_state.DispensationState.dispensed_drugs,
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Drug"),
                                rx.table.column_header_cell("Quantity"),
                                rx.table.column_header_cell("Dispense Date"),
                                rx.table.column_header_cell("Pharmacist"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#ffffff",
                        ),
                        rx.table.body(
                            rx.foreach(
                                dispensation_state.DispensationState.dispensed_drugs,
                                lambda d, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    # rx.table.cell(dispensed_drug.get('drug', {}).get('name', '')),
                                    rx.table.cell(rx.cond(d['quantity'], d['quantity'], '')),
                                    rx.table.cell(rx.cond(d['quantity'], d['quantity'], '')),
                                    rx.table.cell(rx.cond(d['dispense_date'], d['dispense_date'], '')),
                                    rx.table.cell(rx.cond(d['pharmacist_name'], d['pharmacist_name'], '')),
                                    rx.table.cell(
                                        rx.button(
                                            "View Details",
                                            color_scheme="blue",
                                            variant="solid",
                                            size="2",
                                            on_click=lambda d=d: dispensation_state.DispensationState.open_view_modal(d['drug_given_id']),
                                        )
                                    ),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",
                                            "#ffffff",
                                        ),
                                        "color": "#333300",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                )
                            )
                        ),
                        variant="surface",
                    ),
                    width="100%",
                    border_radius="md",
                    overflow="hidden",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("clipboard", size=32, color="grey"),
                        rx.text("No dispensed drugs found", size="3", color="grey"),
                        rx.text("No drugs have been dispensed yet", color="gray"),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    # height="200px",
                    width="100%",
                )
                
            ),
            # View Dispensed Drugs Modal
            create_view_modal(),
            spacing="4",
            width="100%",
            padding="4",
        ),
        width="100%",
    )

def create_dispense_modal():
    """Modal for dispensing drugs."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Dispense Drug"),
            rx.dialog.description("Enter the dispensation details", margin_bottom="1em"),
            rx.vstack(
                rx.text(
                    rx.cond(
                        dispensation_state.DispensationState.selected_prescription,
                        f"Drug: {dispensation_state.DispensationState.selected_prescription.get('drug_name', '')}",
                        ""
                    )
                ),
                rx.input(
                    placeholder="Quantity",
                    value=dispensation_state.DispensationState.quantity,
                    on_change=dispensation_state.DispensationState.set_quantity,
                    type="number",
                ),
                rx.input(
                    placeholder="Dispense Date",
                    value=dispensation_state.DispensationState.dispense_date,
                    on_change=dispensation_state.DispensationState.set_dispense_date,
                    type="date",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=dispensation_state.DispensationState.close_dispense_modal,
                        variant="soft",
                    ),
                    rx.button(
                        rx.cond(
                            dispensation_state.DispensationState.is_dispensation,
                            rx.spinner(size="2", color="white"),
                            rx.text("Dispense", color="white")
                        ),
                        on_click=dispensation_state.DispensationState.dispense_drug,
                        color_scheme="green",
                    ),
                    spacing="3",
                    margin_top="1em",
                ),
                spacing="3",
            ),
            width="90vw",
            max_width="450px",
        ),
        open=dispensation_state.DispensationState.show_dispense_modal,
    )

def create_view_modal():
    """Modal for viewing dispensed drug details."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Dispensed Drug Details"),
            rx.dialog.description("Details of the dispensed drug", margin_bottom="1em"),
            rx.vstack(
                rx.text(
                    rx.cond(
                        dispensation_state.DispensationState.selected_dispensed_drug,
                        f"Drug: {dispensation_state.DispensationState.selected_dispensed_drug.get('drug', {})}",
                        ""
                    )
                ),
                rx.text(
                    rx.cond(
                        dispensation_state.DispensationState.selected_dispensed_drug,
                        f"Quantity: {dispensation_state.DispensationState.selected_dispensed_drug.get('quantity', '')}",
                        ""
                    )
                ),
                rx.text(
                    rx.cond(
                        dispensation_state.DispensationState.selected_dispensed_drug,
                        f"Dispense Date: {dispensation_state.DispensationState.selected_dispensed_drug.get('dispense_date', '')}",
                        ""
                    )
                ),
                rx.text(
                    rx.cond(
                        dispensation_state.DispensationState.selected_dispensed_drug,
                        f"Pharmacist: {dispensation_state.DispensationState.selected_dispensed_drug.get('pharmacist_name', '')}",
                        ""
                    )
                ),
                rx.hstack(
                    rx.button(
                        "Close",
                        on_click=dispensation_state.DispensationState.close_view_modal,
                        variant="soft",
                    ),
                    spacing="3",
                    margin_top="1em",
                ),
                spacing="3",
            ),
            width="90vw",
            max_width="450px",
        ),
        open=dispensation_state.DispensationState.show_view_modal,
    )