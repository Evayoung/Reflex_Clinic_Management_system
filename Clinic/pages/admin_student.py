import reflex as rx
from ..states import admin_student_state


def student_page():
    return rx.center(
        rx.vstack(
            # Header section with search and filters
            rx.hstack(
                # Add Student Button
                rx.button(
                    rx.hstack(
                        rx.icon("plus", size=16),
                        rx.text("Add Student"),
                        spacing="2",
                    ),
                    on_click=admin_student_state.AdminStudentState.set_create_student(True),
                    color="white",
                    bg="linear-gradient(45deg, #330099, #4d4dff)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "transition": "all 0.2s ease-in-out"
                    },
                ),

                # Search and Sort section
                rx.hstack(
                    rx.select(
                        items=["matriculation_number", "name", "faculty_name", "department_name", "level_name"],
                        value=admin_student_state.AdminStudentState.sort_field,
                        on_change=admin_student_state.AdminStudentState.sort_students_by,
                        placeholder="Sort By",
                        width="150px",
                        color_scheme="purple",
                        variant="classic",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Search students...",
                            width="250px",
                            color_scheme="purple",
                            variant="classic",
                            on_change=admin_student_state.AdminStudentState.search_students,
                        ),
                        rx.button(
                            rx.icon("search"),
                            color_scheme="purple",
                            variant="solid",
                            border_radius="0 8px 8px 0",
                        ),
                        spacing="0",
                    ),
                    spacing="4",
                ),

                # Faculty and Department filters
                rx.hstack(
                    rx.select(
                        admin_student_state.AdminStudentState.faculties,
                        value=admin_student_state.AdminStudentState.faculty,
                        on_change=admin_student_state.AdminStudentState.change_faculty,
                        placeholder="All Faculties",
                        width="200px",
                        color_scheme="purple",
                        variant="classic",
                    ),
                    rx.select(
                        admin_student_state.AdminStudentState.departments,
                        value=admin_student_state.AdminStudentState.department,
                        on_change=admin_student_state.AdminStudentState.change_department,
                        placeholder="All Departments",
                        width="250px",
                        color_scheme="purple",
                        variant="classic",
                    ),
                    spacing="4",
                ),
                
                justify="between",
                width="100%",
                padding_y="2",
            ),

            # Student Table/List Section
            rx.box(
                rx.cond(
                    admin_student_state.AdminStudentState.students,
                    # If students exist, show them in a table
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Matric No."),
                                rx.table.column_header_cell("Name"),
                                rx.table.column_header_cell("Faculty"),
                                rx.table.column_header_cell("Department"),
                                rx.table.column_header_cell("Level"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#330099",
                        ),
                        rx.table.body(
                            rx.foreach(
                                admin_student_state.AdminStudentState.paginated_students,
                                lambda student, idx: 
                                rx.table.row(
                                    rx.table.cell(student["matriculation_number"]),
                                    rx.table.cell(f"{student['first_name']} {student['surname']}"),
                                    rx.table.cell(student["faculty_name"]),  # Changed from student["faculty"]
                                    rx.table.cell(student["department_name"]),  # Changed from student["department"]
                                    rx.table.cell(student["level_name"]),  # Changed from student["level"]
                                    rx.table.cell(
                                        rx.badge(
                                            student["status"],
                                            variant="soft",
                                            color_scheme=rx.cond(student["status"] == "active", "green", "red")
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("eye", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=lambda: admin_student_state.AdminStudentState.set_selected_student(student)  # Add this for dialog
                                            ),
                                            rx.button(
                                                rx.icon("pencil", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=lambda: admin_student_state.AdminStudentState.set_edit_student(student),  # Edit student
                                            ),
                                            spacing="2",
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
                    # If no students, show empty state
                    rx.center(
                        rx.vstack(
                            rx.icon("users", size=32),
                            rx.text("No students found", size="4"),
                            rx.text("Add a new student to get started", color="gray"),
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
                    admin_student_state.AdminStudentState.show_choices,
                    value=admin_student_state.AdminStudentState.show_choice,
                    on_change=admin_student_state.AdminStudentState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=admin_student_state.AdminStudentState.prev_page,
                        variant="ghost",
                        disabled=admin_student_state.AdminStudentState.current_page == 1,
                    ),
                    rx.text(f"Page {admin_student_state.AdminStudentState.current_page}",  color="#330099"),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=admin_student_state.AdminStudentState.next_page,
                        variant="ghost",
                        # disabled=admin_student_state.AdminStudentState.current_page * 
                        #         admin_student_state.AdminStudentState.items_per_page >= 
                        #         len(admin_student_state.AdminStudentState.students),
                    ),
                    spacing="2",
                ),
                justify="between",
                width="100%",
                padding_top="4",
            ),

            spacing="4",
            width="100%",

            # max_width="1200px",
            padding="4",
        ),

        # Add the student registration dialog
        create_user(),
        student_details_dialog(),
        width="100%",
        # Fetch students on mount
        # on_mount=admin_student_state.AdminStudentState.get_students,
    )


def create_user():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    admin_student_state.AdminStudentState.is_editing,
                    "Edit Student",
                    "Register New Student"
                ), 
                font_size="1.2em", 
                color="#330099"
                ),
            rx.dialog.description(
                rx.cond(
                    admin_student_state.AdminStudentState.is_editing,
                    "Update student details",
                    "Fill in all required student details"
                ),
                margin_bottom="1em",
                color="#666",
            ),
            rx.scroll_area(
                rx.vstack(
                    # First row - Matric Number and Name
                    rx.hstack(
                        rx.vstack(
                            rx.text("Matric Number", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Enter matric number",
                                value=admin_student_state.AdminStudentState.matriculation_number,
                                on_change=admin_student_state.AdminStudentState.change_matric,
                                disabled=admin_student_state.AdminStudentState.is_editing,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("First Name", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Enter first name",
                                value=admin_student_state.AdminStudentState.first_name,
                                on_change=admin_student_state.AdminStudentState.change_first_name,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Second row - Surname and Email
                    rx.hstack(
                        rx.vstack(
                            rx.text("Surname", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Enter surname",
                                value=admin_student_state.AdminStudentState.surname,
                                on_change=admin_student_state.AdminStudentState.change_surname,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Email", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Enter email",
                                type="email",
                                value=admin_student_state.AdminStudentState.email,
                                on_change=admin_student_state.AdminStudentState.change_email,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Third row - Session and Phone
                    rx.hstack(
                        rx.vstack(
                            rx.text("Session", as_="div", size="2", color="#333"),
                            
                            rx.select(
                                admin_student_state.AdminStudentState.all_sessions,
                                placeholder="Select session",
                                value=admin_student_state.AdminStudentState.session,
                                on_change=admin_student_state.AdminStudentState.change_session,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Phone Number", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Enter phone number",
                                value=admin_student_state.AdminStudentState.phone,
                                on_change=admin_student_state.AdminStudentState.change_phone,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Fourth row - Date of Birth and Gender
                    rx.hstack(
                        rx.vstack(
                            rx.text("Date of Birth", as_="div", size="2", color="#333"),
                            rx.input(
                                type="date",
                                value=admin_student_state.AdminStudentState.date_of_birth,
                                on_change=admin_student_state.AdminStudentState.change_date_of_birth,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Gender", as_="div", size="2", color="#333"),
                            rx.select(
                                admin_student_state.AdminStudentState.genders,
                                placeholder="Select gender",
                                value=admin_student_state.AdminStudentState.gender,
                                on_change=admin_student_state.AdminStudentState.change_gender,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Fifth row - Faculty and Department
                    rx.hstack(
                        rx.vstack(
                            rx.text("Faculty", as_="div", size="2", color="#333"),
                            rx.select(
                                admin_student_state.AdminStudentState.faculties,
                                placeholder="Select faculty",
                                value=admin_student_state.AdminStudentState.faculty,
                                on_change=admin_student_state.AdminStudentState.change_faculty,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Department", as_="div", size="2", color="#333"),
                            rx.select(
                                admin_student_state.AdminStudentState.departments,
                                placeholder="Select department",
                                value=admin_student_state.AdminStudentState.department,
                                on_change=admin_student_state.AdminStudentState.change_department,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Sixth row - Level and Emergency Contact
                    rx.hstack(
                        rx.vstack(
                            rx.text("Level", as_="div", size="2", color="#333"),
                            rx.select(
                                admin_student_state.AdminStudentState.all_levels,
                                placeholder="Select level",
                                value=admin_student_state.AdminStudentState.level,
                                on_change=admin_student_state.AdminStudentState.change_level,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Emergency Contact", as_="div", size="2", color="#333"),
                            rx.input(
                                placeholder="Emergency contact number",
                                value=admin_student_state.AdminStudentState.emergency_contact,
                                on_change=admin_student_state.AdminStudentState.change_emergency_contact,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Seventh row - Address and Password
                    rx.hstack(
                        rx.vstack(
                            rx.text("Address", as_="div", size="2", color="#333"),
                            rx.text_area(
                                placeholder="Enter student address",
                                value=admin_student_state.AdminStudentState.address,
                                on_change=admin_student_state.AdminStudentState.change_address,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        rx.vstack(
                            rx.text("Password", as_="div", size="2", color="#333"),
                            rx.input(
                                type="password",
                                placeholder="Create password",
                                value=admin_student_state.AdminStudentState.password,
                                on_change=admin_student_state.AdminStudentState.change_password,
                                width="100%",
                                required=True,
                            ),
                            width="48%",
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    
                    # Profile Picture Upload
                    rx.vstack(
                        rx.text("Profile Picture (Optional)", as_="div", size="2", color="#333"),
                        rx.upload(
                            rx.text("Drag and drop an image here or click to browse"),
                            id="upload_passport",
                            max_files=1,
                            accept="image/*",
                            on_drop=admin_student_state.AdminStudentState.handle_upload(rx.upload_files(upload_id="upload_passport")),
                            border="1px dashed #330099",
                            padding="1em",
                            width="100%",
                        ),
                        rx.text(rx.selected_files("upload_passport")),
                        width="100%",
                        padding="0",
                    ),
                    
                    spacing="3",
                    width="100%",
                ),
                type="always",
                scrollbars="vertical",
                style={"height": "60vh", "padding": "0 1em"},
            ),
            
            # Dialog footer with action buttons
            rx.flex(
                rx.button(
                    "Cancel",
                    variant="soft",
                    color_scheme="gray",
                    on_click=admin_student_state.AdminStudentState.set_create_student(False),
                ),
                rx.button(
                    rx.cond(
                        admin_student_state.AdminStudentState.is_student,
                        rx.spinner(size="2", color="white"),
                        rx.cond(
                            admin_student_state.AdminStudentState.is_editing,
                            "Update Student",
                            "Register Student"
                        )
                    ),
                    variant="solid",
                    color_scheme="purple",
                    on_click=rx.cond(
                        admin_student_state.AdminStudentState.is_editing,
                        admin_student_state.AdminStudentState.update_student,
                        admin_student_state.AdminStudentState.register_student
                    ),
                    disabled=admin_student_state.AdminStudentState.is_student,
                ),
                spacing="3",
                margin_top="1em",
                justify="end",
            ),
            style={"max_width": "800px"},
        ),
        open=admin_student_state.AdminStudentState.create_student,
    )


def student_details_dialog():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Student Details", font_size="1.2em", color="#330099"),
            rx.dialog.description(
                "View student information",
                margin_bottom="1em",
                color="#666",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.hstack(
                        rx.text("Matric Number:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["matriculation_number"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Name:", weight="bold", color="#333"),
                        rx.text(f"{admin_student_state.AdminStudentState.selected_student['first_name']} {admin_student_state.AdminStudentState.selected_student['surname']}"),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Email:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["email"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Session:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["session_name"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Phone:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["phone"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Date of Birth:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["date_of_birth"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Gender:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["gender"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Faculty:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["faculty_name"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Department:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["department_name"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Level:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["level_name"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Emergency Contact:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["emergency_contact"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Address:", weight="bold", color="#333"),
                        rx.text(admin_student_state.AdminStudentState.selected_student["address"]),
                        width="100%",
                        spacing="4",
                    ),
                    rx.hstack(
                        rx.text("Status:", weight="bold", color="#333"),
                        rx.badge(
                            admin_student_state.AdminStudentState.selected_student["status"],
                            variant="soft",
                            color_scheme=rx.cond(
                                admin_student_state.AdminStudentState.selected_student["status"] == "active",
                                "green",
                                "red"
                            )    
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    rx.cond(
                        admin_student_state.AdminStudentState.selected_student["profile_picture"],
                        rx.image(
                            src=admin_student_state.AdminStudentState.selected_student["profile_picture"],
                            width="100px",
                            height="100px",
                            border_radius="50%",
                            margin_top="1em",
                        ),
                        rx.text("No profile picture", color="#666"),
                    ),
                    spacing="3",
                    width="100%",
                ),
                type="always",
                scrollbars="vertical",
                style={"height": "60vh", "padding": "0 1em"},
            ),
            rx.flex(
                rx.button(
                    "Close",
                    variant="soft",
                    color_scheme="gray",
                    on_click=admin_student_state.AdminStudentState.set_show_student_dialog(False),
                ),
                spacing="3",
                margin_top="1em",
                justify="end",
            ),
            style={"max_width": "800px"},
        ),
        open=admin_student_state.AdminStudentState.show_student_dialog,
    )
