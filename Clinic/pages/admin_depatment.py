import reflex as rx
from ..states import admin_student_state, admin_department_state


def department_page():
    return rx.center(
        rx.vstack(
            # Header section with search and filters
            rx.hstack(
                # Add Faculty Button (now handled by the dialog trigger)
                create_department_dialog(),
                rx.select(
                    admin_department_state.AdminDepartmentState.all_faculties,
                    value=admin_department_state.AdminDepartmentState.sort_field,
                    on_change=admin_department_state.AdminDepartmentState.sort_department_by,
                    placeholder="Sort By",
                    width="300px",
                    color_scheme="purple",
                    variant="classic",
                ),
                # rx.select(
                #     admin_department_state.AdminDepartmentState.all_faculties,
                #     value=admin_department_state.AdminDepartmentState.selected_faculty_name,
                #     on_change=admin_department_state.AdminDepartmentState.set_selected_faculty,
                #     placeholder="Select Faculty",
                # ),
                
                # Search and Sort section
                rx.hstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Search department...",
                            width="250px",
                            color_scheme="purple",
                            variant="classic",
                            value=admin_department_state.AdminDepartmentState.search_query,
                            on_change=admin_department_state.AdminDepartmentState.set_search_query,
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
                
                justify="between",
                width="100%",
                padding_y="2",
            ),

            # Faculty Table/List Section
            rx.box(
                rx.cond(
                    admin_department_state.AdminDepartmentState.departments,
                    # If faculties exist, show them in a table
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Department Name"),
                                rx.table.column_header_cell("Faculty"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#330099",
                        ),
                        rx.table.body(
                            rx.foreach(
                                admin_department_state.AdminDepartmentState.paginated_departments,
                                lambda department, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(department["department_name"]),
                                    rx.table.cell(department["faculty_name"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=admin_department_state.AdminDepartmentState.open_dialog(department),
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
                    # If no faculties, show empty state
                    rx.center(
                        rx.vstack(
                            rx.icon("school", size=32),
                            rx.text("No faculties found", size="4"),
                            rx.text("Add a new faculty to get started", color="gray"),
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
                    admin_department_state.AdminDepartmentState.show_choices,
                    value=admin_department_state.AdminDepartmentState.show_choice,
                    on_change=admin_department_state.AdminDepartmentState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=admin_department_state.AdminDepartmentState.prev_page,
                        variant="ghost",
                        disabled=admin_department_state.AdminDepartmentState.current_page == 1,
                    ),
                    rx.text(f"Page {admin_department_state.AdminDepartmentState.current_page} of {admin_department_state.AdminDepartmentState.total_pages}", color="#330099"),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=admin_department_state.AdminDepartmentState.next_page,
                        variant="ghost",
                        disabled=admin_department_state.AdminDepartmentState.current_page >= admin_department_state.AdminDepartmentState.total_pages,
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
        width="100%",
        # on_mount=admin_faculty_state.AdminFacultyState.get_faculties,
    )

def create_department_dialog():
    """Dialog for creating/editing departments."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(rx.icon("plus"), rx.text("New Department")),
                on_click=admin_department_state.AdminDepartmentState.open_dialog(None),
                color_scheme="purple"
            )
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    admin_department_state.AdminDepartmentState.is_editing,
                    "Edit Department",
                    "Create New Department"
                )
            ),
            rx.dialog.description(
                "Enter department details",
                margin_bottom="2"
            ),
            rx.vstack(
                rx.input(
                    placeholder="Department Name",
                    value=admin_department_state.AdminDepartmentState.department_name,
                    on_change=admin_department_state.AdminDepartmentState.set_department_name,
                ),
                rx.select(
                    admin_department_state.AdminDepartmentState.all_faculties,
                    value=admin_department_state.AdminDepartmentState.selected_faculty_name,
                    on_change=admin_department_state.AdminDepartmentState.set_selected_faculty,
                    placeholder="Select Faculty",
                ),
                rx.hstack(
                    rx.button("Cancel", 
                        on_click=admin_department_state.AdminDepartmentState.close_dialog,
                        variant="soft"
                    ),
                    rx.button(
                        rx.cond(
                            admin_department_state.AdminDepartmentState.create_department,
                            rx.spinner(),
                            rx.cond(
                                admin_department_state.AdminDepartmentState.is_editing,
                                "Update",
                                "Create"
                            )
                        ),
                        on_click=admin_department_state.AdminDepartmentState.submit_department,
                        color_scheme="purple"
                    ),
                    spacing="3"
                ),
                spacing="4"
            ),
            width="90vw",
            max_width="450px"
        ),
        open=admin_department_state.AdminDepartmentState.show_dialog
    )

