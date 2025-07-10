import reflex as rx
from ..states.doctor_availability_state import DoctorAvailabilityState


def availability_page():
    return rx.center(
        rx.vstack(
            # Header section
            rx.hstack(
                create_availability_dialog(),
                rx.hstack(
                    rx.input(
                        placeholder="Search availability...",
                        width="250px",
                        color_scheme="purple",
                        variant="classic",
                        value=DoctorAvailabilityState.search_query,
                        on_change=DoctorAvailabilityState.set_search_query,
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

            # Availability Table
            rx.box(
                rx.cond(
                    DoctorAvailabilityState.availabilities,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Day"),
                                rx.table.column_header_cell("Start Time"),
                                rx.table.column_header_cell("End Time"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="white",
                        ),
                        rx.table.body(
                            rx.foreach(
                                DoctorAvailabilityState.paginated_availabilities,
                                lambda avail, idx: rx.table.row(
                                    rx.table.cell(avail["day_of_week"]),
                                    rx.table.cell(avail["start_time"]),
                                    rx.table.cell(avail["end_time"]),
                                    rx.table.cell(avail["status"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=DoctorAvailabilityState.open_dialog(avail),
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
                            rx.icon("calendar", size=32),
                            rx.text("No availability schedules found", size="4"),
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

            # Pagination Controls
            rx.hstack(
                rx.select(
                    DoctorAvailabilityState.show_choices,
                    value=DoctorAvailabilityState.show_choice,
                    on_change=DoctorAvailabilityState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=DoctorAvailabilityState.prev_page,
                        variant="ghost",
                        disabled=DoctorAvailabilityState.current_page == 1,
                    ),
                    rx.text(
                        f"Page {DoctorAvailabilityState.current_page} of {DoctorAvailabilityState.total_pages}", 
                        color="#330099"
                    ),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=DoctorAvailabilityState.next_page,
                        variant="ghost",
                        disabled=DoctorAvailabilityState.current_page >= DoctorAvailabilityState.total_pages,
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
        on_mount=DoctorAvailabilityState.on_mount,
    )


def create_availability_dialog():
    """Enhanced dialog with validation"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(rx.icon("plus"), rx.text("New Schedule")),
                on_click=DoctorAvailabilityState.open_dialog(None),
                color_scheme="purple"
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Manage Availability"),
            rx.vstack(
                rx.select(
                    DoctorAvailabilityState.week_days,
                    value=DoctorAvailabilityState.day_of_week,
                    on_change=DoctorAvailabilityState.set_day_of_week,
                    placeholder="Select Day",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("Start Time", size="2"),
                        rx.input(
                            type="time",
                            value=DoctorAvailabilityState.start_time,
                            on_change=DoctorAvailabilityState.set_start_time,
                        ),
                        align_items="start"
                    ),
                    rx.vstack(
                        rx.text("End Time", size="2"),
                        rx.input(
                            type="time",
                            value=DoctorAvailabilityState.end_time,
                            on_change=DoctorAvailabilityState.set_end_time,
                        ),
                        align_items="start"
                    ),
                    width="100%",
                    spacing="4"
                ),
                rx.select(
                    DoctorAvailabilityState.all_status,
                    value=DoctorAvailabilityState.status,
                    on_change=DoctorAvailabilityState.set_status,
                    placeholder="Select Status",
                ),
                rx.cond(
                    DoctorAvailabilityState.start_time >= DoctorAvailabilityState.end_time,
                    rx.text(
                        "End time must be after start time",
                        color="red",
                        size="1"
                    )
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=DoctorAvailabilityState.close_dialog,
                        variant="soft"
                    ),
                    rx.button(
                        rx.cond(
                            DoctorAvailabilityState.creating_availability,
                            rx.spinner(),
                            rx.cond(
                                DoctorAvailabilityState.is_editing,
                                "Update",
                                "Create"
                            )
                        ),
                        on_click=DoctorAvailabilityState.submit_availability,
                        color_scheme="purple",
                        is_disabled=(
                            DoctorAvailabilityState.start_time >= 
                            DoctorAvailabilityState.end_time
                        )
                    ),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),
                spacing="4"
            ),
            width="90vw",
            max_width="450px"
        ),
        open=DoctorAvailabilityState.show_dialog
    )