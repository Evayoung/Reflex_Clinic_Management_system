import reflex as rx
from ..states import doctor_schedule_state, doctor_visit_state, doctor_state

def visit_page():
    return rx.box(
        rx.cond(
            doctor_visit_state.DoctorVisitState.current_vist_view == "Visit List",
            rx.vstack(
                # Header section - identical structure to availability
                rx.hstack(
                    # create_visit_dialog(),
                    rx.hstack(
                        rx.input(
                            placeholder="Search schedules...",
                            width="250px",
                            color_scheme="purple",
                            variant="classic",
                            value=doctor_visit_state.DoctorVisitState.search_query,
                            on_change=doctor_visit_state.DoctorVisitState.set_search_query,
                        ),
                        rx.button(
                            rx.icon("search"),
                            color_scheme="purple",
                            variant="solid",
                            border_radius="0 8px 8px 0",
                        ),
                        spacing="0",
                    ),
                    justify="between",
                    width="100%",
                    padding_y="2",
                ),

                # Schedule Table - same styling as availability
                rx.box(
                    rx.cond(
                        doctor_visit_state.DoctorVisitState.pending,
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Student Name"),
                                    rx.table.column_header_cell("Matric No."),
                                    rx.table.column_header_cell("visit Date"),
                                    rx.table.column_header_cell("Time Slot"),
                                    rx.table.column_header_cell("Complaints"),
                                    rx.table.column_header_cell("Actions"),
                                ),
                                background_color="#330099",
                                color="white",
                            ),
                            
                            rx.table.body(
                                rx.foreach(
                                    doctor_visit_state.DoctorVisitState.paginated_appointment,
                                    lambda visit, idx: rx.table.row(
                                        rx.table.cell(visit["student_name"]),
                                        rx.table.cell(visit["matric_number"]),
                                        rx.table.cell(visit["visit_date"]),
                                        rx.table.cell(visit["time_slot"]),
                                        rx.table.cell(visit["complaint_description"]),
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.button(
                                                    rx.icon("pencil", size=14),
                                                    variant="ghost",
                                                    size="1",
                                                    on_click=doctor_visit_state.DoctorVisitState.edit_selected_student(visit["visit_id"]),
                                                    
                                                ),
                                                rx.button(
                                                    rx.icon("eye", size=14),
                                                    variant="ghost",
                                                    size="1",
                                                    on_click=doctor_visit_state.DoctorVisitState.view_selected_student(visit["visit_id"]),
                                                    
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
                        # Empty state - same styling
                        rx.center(
                            rx.vstack(
                                rx.icon("calendar", size=32),
                                rx.text("No schedules found", size="4"),
                                rx.text("Add a new schedule to get started", color="gray"),
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

                # Pagination Controls - identical to availability
                rx.hstack(
                    rx.select(
                        doctor_visit_state.DoctorVisitState.show_choices,
                        value=doctor_visit_state.DoctorVisitState.show_choice,
                        on_change=doctor_visit_state.DoctorVisitState.change_items_per_page,
                        width="80px",
                        size="1",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.icon("chevron-left", color="#330099"),
                            on_click=doctor_visit_state.DoctorVisitState.prev_page,
                            variant="ghost",
                            disabled=doctor_visit_state.DoctorVisitState.current_page == 1,
                        ),
                        rx.text(
                            f"Page {doctor_visit_state.DoctorVisitState.current_page} of {doctor_visit_state.DoctorVisitState.total_pages}", 
                            color="#330099"
                        ),
                        rx.button(
                            rx.icon("chevron-right", color="#330099"),
                            on_click=doctor_visit_state.DoctorVisitState.next_page,
                            variant="ghost",
                            disabled=doctor_visit_state.DoctorVisitState.current_page >= doctor_visit_state.DoctorVisitState.total_pages,
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
                overflow="hidden",
            ),
            
        ),
        rx.cond(
            doctor_visit_state.DoctorVisitState.current_vist_view == "View Visit",
            rx.vstack(
                rx.heading("Visit Details", size="5", color="grey"),
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Student:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("full_name", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Gender:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("gender", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Matric No:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("matric_number", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Faculty:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("faculty", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Department:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("department", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Level:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.student_visit.get("level", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Visit Date:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.visit_data.get("visit_date", ""), color="black"),
                            width="100%"
                        ),
                        spacing="3"
                    ),
                    width="100%"
                ),
                
                # Diagnosis Section
                rx.card(
                    rx.vstack(
                        rx.vstack(
                            rx.heading("Complaint", size="3", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.visit_complaint.get("complaint_description", ""), color="#330099"),
                            width="100%",
                            justify="start",
                            spacing="1"
                        ),
                        rx.vstack(
                            rx.heading("Diagnosis", size="3", color="grey"),
                            rx.text(
                                rx.cond(
                                    doctor_visit_state.DoctorVisitState.visit_diagnosis == None,
                                    "No Data",
                                    doctor_visit_state.DoctorVisitState.visit_diagnosis.get("diagnosis_description", ""), 
                                    ),
                                color="#330099"
                                ),
                            width="100%",
                            justify="start",
                            spacing="1"
                        ),
                        rx.vstack(
                            rx.heading("Treatment Plane", size="3", color="grey"),
                            rx.text(
                                rx.cond(
                                    doctor_visit_state.DoctorVisitState.visit_diagnosis == None,
                                    "No Data",
                                    doctor_visit_state.DoctorVisitState.visit_diagnosis.get("treatment_plan", ""), 
                                    ),
                                color="#330099"
                                ),
                            width="100%",
                            justify="start",
                            spacing="1"
                        ),
                        width="100%",
                        spacing="3"
                    ),
                    width="100%"
                ),
                
                # Prescriptions Section
                rx.card(
                    rx.vstack(
                        rx.heading("Prescriptions", size="5", color="grey"),
                        rx.foreach(
                            doctor_visit_state.DoctorVisitState.visit_prescription,
                            lambda prescription: rx.card(
                                rx.vstack(
                                    rx.text(f"Drug: {prescription['drug_name']}", color="#330099"),
                                    rx.text(f"Dosage: {prescription['dosage']}", color="#330099"),
                                    rx.text(f"Instructions: {prescription['instructions']}", color="#330099"),
                                    spacing="2"
                                )
                            )
                        ),
                        width="100%",
                        justify="start"
                    ),
                    width="100%"
                ),
                
                # Back button
                rx.button(
                    "Back to List",
                    on_click=lambda: doctor_visit_state.DoctorVisitState.change_visit_view("Visit List"),
                    variant="soft"
                ),
                spacing="4",
                width="100%",
                padding="4",
                overflow_y="auto",
                overflow_x="hidden",
                style={
                    "scrollbar_width": "thin",
                    "scrollbar_color": "transparent transparent",  # Makes it very subtle
                    "&::-webkit-scrollbar": {
                        "width": "6px",
                    },
                    "&::-webkit-scrollbar-thumb": {
                        "background": "rgba(0,0,0,0.2)",  # Semi-transparent
                        "border_radius": "3px",
                    },
                }
            ),
        ),
        rx.cond(
            doctor_visit_state.DoctorVisitState.current_vist_view == "Create Visit",
            rx.vstack(
                rx.heading("Create New Visit", size="5", color="grey"),
                
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Student:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.selected_student.get("student_name", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Matric No:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.selected_student.get("matric_number", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Visit Date:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.selected_student.get("visit_date", ""), color="black"),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.text("Complaint:", weight="bold", color="grey"),
                            rx.text(doctor_visit_state.DoctorVisitState.selected_student.get("complaint_description", ""), color="black"),
                            width="100%"
                        ),
                        spacing="3"
                    ),
                    width="100%"
                ),
                
                # Diagnosis Section
                rx.card(
                    rx.vstack(
                        rx.heading("Doctor Assessment", size="5", color="grey"),
                        rx.cond(
                            doctor_visit_state.DoctorVisitState.loaded_diagnosis,
                            rx.vstack(
                                rx.text("Diagnosis:", weight="bold", color="grey"),
                                rx.text(doctor_visit_state.DoctorVisitState.loaded_diagnosis.get("diagnosis_description"), color="black", margin_bottom="1.5rem"),
                                rx.text("Treatment Plan:", weight="bold", color="grey"),
                                rx.text(doctor_visit_state.DoctorVisitState.loaded_diagnosis.get("treatment_plan", ""), color="black"),
                                spacing="2"
                            ),
                            rx.vstack(
                                rx.text("No diagnosis yet", color="gray"),
                                rx.button(
                                    "Add Diagnosis",
                                    on_click=doctor_visit_state.DoctorVisitState.open_diagnosis_dialog,
                                    color_scheme="purple"
                                ),
                                spacing="2"
                            )
                        ),
                        width="100%",
                        justify="start"
                    ),
                    width="100%"
                ),
                # Prescriptions Section
                rx.card(
                    rx.vstack(
                        rx.heading("Prescriptions", size="5", color="grey"),
                        rx.foreach(
                            doctor_visit_state.DoctorVisitState.prescriptions,
                            lambda prescription: rx.card(
                                rx.vstack(
                                    rx.text(f"Drug: {doctor_visit_state.DoctorVisitState.drug}", color="#330099", size="2"),
                                    rx.text(f"Dosage: {prescription['dosage']}", color="#330099", size="2"),
                                    rx.text(f"Instructions: {prescription['instructions']}", color="#330099", size="2"),
                                    rx.hstack(
                                        rx.icon(
                                            "trash", 
                                            color="red", 
                                            size=16, 
                                            cursor="pointer",
                                            on_click=doctor_visit_state.DoctorVisitState.delete_prescription(prescription)
                                            ), 
                                        justify="end",
                                        width="100%"
                                        ),
                                    spacing="2",
                                    width="100%"
                                )
                            )
                        ),
                        width="100%",
                        justify="start"
                    ),
                    width="100%"
                ),

                # Update the "Add Prescription" section
                rx.card(
                    rx.vstack(
                        rx.heading("Add Prescription", size="5", color="grey"),
                        rx.select(
                            doctor_visit_state.DoctorVisitState.drugs,
                            placeholder="Select Drug",
                            value=doctor_visit_state.DoctorVisitState.drug,
                            on_change=doctor_visit_state.DoctorVisitState.set_drug_id,
                            width="100%"
                        ),
                        rx.input(
                            placeholder="Dosage",
                            value=doctor_visit_state.DoctorVisitState.dosage,
                            on_change=doctor_visit_state.DoctorVisitState.set_dosage,
                            width="100%"
                        ),
                        rx.text_area(
                            placeholder="Instructions",
                            value=doctor_visit_state.DoctorVisitState.instruction,
                            on_change=doctor_visit_state.DoctorVisitState.set_instruction,
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button(
                                "Add",
                                on_click=doctor_visit_state.DoctorVisitState.add_prescription,
                                color_scheme="purple",
                                is_loading=doctor_visit_state.DoctorVisitState.is_prescriptions
                            ),
                            rx.button(
                                rx.cond(
                                    doctor_visit_state.DoctorVisitState.is_prescriptions,
                                    rx.spinner(size="2", color="white"),
                                    rx.text("Submit all prescriptions", color="white")
                                ),
                                on_click=doctor_visit_state.DoctorVisitState.save_prescriptions,
                                color_scheme="purple"
                            ),
                            width="100%",
                            justify="end",
                            spacing="4"
                        ),
                        spacing="3"
                    ),
                    width="100%"
                ),
                

                rx.button(
                    "Back to List",
                    on_click=lambda: doctor_visit_state.DoctorVisitState.change_visit_view("Visit List"),
                    variant="soft"
                ),
                create_Diagnosis_dialog(),
                spacing="4",
                width="100%",
                padding="4",
                overflow_y="auto",
                overflow_x="hidden",
            ),
        ),
        width="100%",
        height="600px",
        overflow_y="auto",
    )


def create_Diagnosis_dialog():
    """Dialog for creating/editing Diagnosis."""
    return rx.dialog.root(
        
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    doctor_visit_state.DoctorVisitState.edit_diagnosis,
                    "Edit Diganosis",
                    "Add Diagnosis"
                )
            ),
            rx.dialog.description(
                "Fill in the details of your diagnosis",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.text_area(
                    placeholder="Enter diagnosis...",
                    value=doctor_visit_state.DoctorVisitState.current_diagnosis,
                    on_change=doctor_visit_state.DoctorVisitState.set_current_diagnosis,
                    width="100%",
                ),
                rx.text_area(
                    placeholder="Treatment plan...",
                    value=doctor_visit_state.DoctorVisitState.current_treatment_plan,
                    on_change=doctor_visit_state.DoctorVisitState.set_current_treatment_plan,
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=doctor_visit_state.DoctorVisitState.close_diagnosis_dialog,
                        variant="soft",
                    ),
                    rx.button(
                        rx.cond(
                            doctor_visit_state.DoctorVisitState.edit_diagnosis,
                            rx.cond(
                                doctor_visit_state.DoctorVisitState.is_diagnosis,
                                rx.spinner(size="2", color="white"),
                                rx.text("Update Diagnosis", color="white")
                            ),
                            rx.cond(
                                doctor_visit_state.DoctorVisitState.is_diagnosis,
                                rx.spinner(size="2", color="white"),
                                rx.text("Save Diagnosis", color="white")
                            ),
                            
                        ),
                        on_click=doctor_visit_state.DoctorVisitState.create_diagnosis,
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
        open=doctor_visit_state.DoctorVisitState.add_diagnosis,
    )

