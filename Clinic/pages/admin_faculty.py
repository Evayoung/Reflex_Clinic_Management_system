import reflex as rx
from ..states import admin_student_state, admin_faculty_state


def faculty_page():
    return rx.box(
        rx.vstack(
            # Header section with search and filters
            rx.hstack(
                # Add Faculty Button (now handled by the dialog trigger)
                create_faculty_dialog(),
                
                # Search and Sort section
                rx.hstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Search faculty...",
                            width="250px",
                            color_scheme="purple",
                            variant="classic",
                            value=admin_faculty_state.AdminFacultyState.search_query,
                            on_change=admin_faculty_state.AdminFacultyState.set_search_query,
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
                    admin_faculty_state.AdminFacultyState.faculties,
                    # If faculties exist, show them in a table
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Faculty Name"),
                                rx.table.column_header_cell("Faculty Type"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#330099",
                        ),
                        rx.table.body(
                            rx.foreach(
                                admin_faculty_state.AdminFacultyState.paginated_faculties,
                                lambda faculty, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(faculty["faculty_name"]),
                                    rx.table.cell(faculty["faculty_type"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=admin_faculty_state.AdminFacultyState.open_dialog(faculty),
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
                    admin_faculty_state.AdminFacultyState.show_choices,
                    value=admin_faculty_state.AdminFacultyState.show_choice,
                    on_change=admin_faculty_state.AdminFacultyState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=admin_faculty_state.AdminFacultyState.prev_page,
                        variant="ghost",
                        disabled=admin_faculty_state.AdminFacultyState.current_page == 1,
                    ),
                    rx.text(f"Page {admin_faculty_state.AdminFacultyState.current_page} of {admin_faculty_state.AdminFacultyState.total_pages}", color="#330099"),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=admin_faculty_state.AdminFacultyState.next_page,
                        variant="ghost",
                        disabled=admin_faculty_state.AdminFacultyState.current_page >= admin_faculty_state.AdminFacultyState.total_pages,
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

def create_faculty_dialog():
    """Dialog for creating/editing faculties."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("New Faculty"),
                    spacing="2",
                ),
                on_click=admin_faculty_state.AdminFacultyState.open_dialog(None),
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
                    admin_faculty_state.AdminFacultyState.is_editing,
                    "Edit Faculty",
                    "Create New Faculty"
                )
            ),
            rx.dialog.description(
                "Fill in the details for the faculty",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Faculty Name",
                    value=admin_faculty_state.AdminFacultyState.faculty_name,
                    on_change=admin_faculty_state.AdminFacultyState.set_faculty_name,
                ),
                rx.select(
                    admin_faculty_state.AdminFacultyState.faculty_types,
                    value=admin_faculty_state.AdminFacultyState.faculty_type,
                    on_change=admin_faculty_state.AdminFacultyState.set_faculty_type,
                    placeholder="Select faculty type",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=admin_faculty_state.AdminFacultyState.close_dialog,
                        variant="soft",
                    ),
                    rx.button(
                        rx.cond(
                            admin_faculty_state.AdminFacultyState.is_editing,
                            rx.cond(
                                admin_faculty_state.AdminFacultyState.create_faculty,
                                rx.spinner(size="2", color="white"),
                                "Update Faculty"
                            ),
                            rx.cond(
                                admin_faculty_state.AdminFacultyState.create_faculty,
                                rx.spinner(size="2", color="white"),
                                "Create Faculty"
                            ),
                            
                        ),
                        on_click=admin_faculty_state.AdminFacultyState.submit_faculty,
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
        open=admin_faculty_state.AdminFacultyState.show_dialog,
    )