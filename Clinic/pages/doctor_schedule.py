import reflex as rx
from ..states import doctor_schedule_state

def schedule_page():
    return rx.center(
        rx.vstack(
            # Header section - identical structure to availability
            rx.hstack(
                create_schedule_dialog(),
                rx.hstack(
                    rx.input(
                        placeholder="Search schedules...",
                        width="250px",
                        color_scheme="purple",
                        variant="classic",
                        value=doctor_schedule_state.DoctorScheduleState.search_query,
                        on_change=doctor_schedule_state.DoctorScheduleState.set_search_query,
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
                    doctor_schedule_state.DoctorScheduleState.schedules,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Date"),
                                rx.table.column_header_cell("Time"),
                                rx.table.column_header_cell("Day of Week"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="white",
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                doctor_schedule_state.DoctorScheduleState.paginated_schedules,
                                lambda schedule, idx: rx.table.row(
                                    rx.table.cell(schedule["date"]),
                                    rx.table.cell(f"{schedule.get('start_time', '')} - {schedule.get('end_time', '')}"),
                                    rx.table.cell(f"{schedule.get('day_of_week', '')}"),
                                    rx.table.cell(schedule["status"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            # rx.button(
                                            #     rx.icon("pencil", size=14),
                                            #     variant="ghost",
                                            #     size="1",
                                            #     on_click=doctor_schedule_state.DoctorScheduleState.open_dialog(schedule),
                                            # ),
                                            rx.button(
                                                rx.icon("x", size=14),
                                                variant="ghost",
                                                size="1",
                                                on_click=doctor_schedule_state.DoctorScheduleState.cancel_schedule(schedule["schedule_id"]),
                                                is_disabled=schedule["status"] != "pending",
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
                    doctor_schedule_state.DoctorScheduleState.show_choices,
                    value=doctor_schedule_state.DoctorScheduleState.show_choice,
                    on_change=doctor_schedule_state.DoctorScheduleState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=doctor_schedule_state.DoctorScheduleState.prev_page,
                        variant="ghost",
                        disabled=doctor_schedule_state.DoctorScheduleState.current_page == 1,
                    ),
                    rx.text(
                        f"Page {doctor_schedule_state.DoctorScheduleState.current_page} of {doctor_schedule_state.DoctorScheduleState.total_pages}", 
                        color="#330099"
                    ),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=doctor_schedule_state.DoctorScheduleState.next_page,
                        variant="ghost",
                        disabled=doctor_schedule_state.DoctorScheduleState.current_page >= doctor_schedule_state.DoctorScheduleState.total_pages,
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
        # on_mount=doctor_schedule_state.DoctorScheduleState.on_mount,
    )


def create_schedule_dialog():
    """Dialog matching availability style exactly"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(rx.icon("plus"), rx.text("New Schedule")),
                on_click=doctor_schedule_state.DoctorScheduleState.open_dialog(None),
                color_scheme="purple"
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Manage Schedule"),
            rx.vstack(
                # Availability Select (matches the simple select pattern from availability)
                rx.hstack(
                    rx.select(
                        doctor_schedule_state.DoctorScheduleState.all_availabilities,
                        value=doctor_schedule_state.DoctorScheduleState.selected_availability_id,
                        on_change=doctor_schedule_state.DoctorScheduleState.set_selected_availability_id,
                        placeholder="Select Availability Slot",
                    ),
                    rx.text(f"{doctor_schedule_state.DoctorScheduleState.day}: {doctor_schedule_state.DoctorScheduleState.show_start} to {doctor_schedule_state.DoctorScheduleState.show_stop}", size="2"),
                    spacing="4"
                ),
                
                # Date Input (added label like availability)
                rx.vstack(
                    rx.text("Schedule Date", size="2"),
                    rx.input(
                        type="date",
                        value=doctor_schedule_state.DoctorScheduleState.schedule_date,
                        on_change=doctor_schedule_state.DoctorScheduleState.set_schedule_date,
                    ),
                    align_items="start",
                    width="100%"
                ),
                
                # Time Inputs (exact same structure as availability)
                rx.hstack(
                    rx.vstack(
                        rx.text("Start Time", size="2"),
                        rx.input(
                            type="time",
                            value=doctor_schedule_state.DoctorScheduleState.start_time,
                            on_change=doctor_schedule_state.DoctorScheduleState.set_start_time,
                        ),
                        align_items="start"
                    ),
                    rx.vstack(
                        rx.text("End Time", size="2"),
                        rx.input(
                            type="time",
                            value=doctor_schedule_state.DoctorScheduleState.end_time,
                            on_change=doctor_schedule_state.DoctorScheduleState.set_end_time,
                        ),
                        align_items="start"
                    ),
                    width="100%",
                    spacing="4"
                ),
                
                # Validation message (same style)
                rx.cond(
                    doctor_schedule_state.DoctorScheduleState.start_time >= doctor_schedule_state.DoctorScheduleState.end_time,
                    rx.text(
                        "End time must be after start time",
                        color="red",
                        size="1"
                    )
                ),
                
                # Action buttons (identical structure)
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=doctor_schedule_state.DoctorScheduleState.close_dialog,
                        variant="soft"
                    ),
                    rx.button(
                        rx.cond(
                            doctor_schedule_state.DoctorScheduleState.creating_schedule,
                            rx.spinner(),
                            rx.cond(
                                doctor_schedule_state.DoctorScheduleState.is_editing,
                                "Update",
                                "Create"
                            )
                        ),
                        on_click=doctor_schedule_state.DoctorScheduleState.submit_schedule,
                        color_scheme="purple",
                        # is_disabled=(
                        #     doctor_schedule_state.DoctorScheduleState.start_time >= 
                        #     doctor_schedule_state.DoctorScheduleState.end_time |
                        #     ~ doctor_schedule_state.DoctorScheduleState.schedule_date |
                        #     ~ doctor_schedule_state.DoctorScheduleState.selected_availability_id
                        # )
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
        # Removed on_open_change to match availability dialog
        open=doctor_schedule_state.DoctorScheduleState.show_dialog
    )