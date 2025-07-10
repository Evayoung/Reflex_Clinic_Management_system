import reflex as rx
from ..states import admin_faculty_state, pharmercy_drug_state


def drug_page():
    return rx.center(
        rx.vstack(
            # Header section with search and filters
            rx.hstack(
                # Add Faculty Button (now handled by the dialog trigger)
                create_drug_dialog(),
                confirm_delete(),
                # Search and Sort section
                rx.hstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Search drug...",
                            width="250px",
                            color_scheme="purple",
                            variant="classic",
                            value=pharmercy_drug_state.PharmercyDrugState.search_query,
                            on_change=pharmercy_drug_state.PharmercyDrugState.set_search_query,
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
                    pharmercy_drug_state.PharmercyDrugState.drugs,
                    # If faculties exist, show them in a table
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("S/N"),
                                rx.table.column_header_cell("Drug Name"),
                                rx.table.column_header_cell("Stock Level"),
                                rx.table.column_header_cell("Descriptions"),
                                rx.table.column_header_cell("Actions"),
                            ),
                            background_color="#330099",
                            color="#330099",
                        ),
                        rx.table.body(
                            rx.foreach(
                                pharmercy_drug_state.PharmercyDrugState.paginated_drugs,
                                lambda drug, idx: rx.table.row(
                                    rx.table.cell(idx + 1),
                                    rx.table.cell(drug["name"]),
                                    rx.table.cell(drug["stock_level"]),
                                    rx.table.cell(drug["description"]),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=16),
                                                variant="ghost",
                                                size="1",
                                                on_click=pharmercy_drug_state.PharmercyDrugState.open_dialog(drug),
                                            ),
                                            rx.button(
                                                rx.icon("trash", size=16),
                                                variant="ghost",
                                                size="1",
                                                on_click=pharmercy_drug_state.PharmercyDrugState.open_delete_drug_dialog(drug["drug_id"]),
                                            ),
                                            
                                            spacing="4",
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
                            rx.icon("pill=bottle", size=32),
                            rx.text("No drugs found", size="4"),
                            rx.text("Add a new drug to get started", color="gray"),
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
                    pharmercy_drug_state.PharmercyDrugState.show_choices,
                    value=pharmercy_drug_state.PharmercyDrugState.show_choice,
                    on_change=pharmercy_drug_state.PharmercyDrugState.change_items_per_page,
                    width="80px",
                    size="1",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("chevron-left", color="#330099"),
                        on_click=pharmercy_drug_state.PharmercyDrugState.prev_page,
                        variant="ghost",
                        disabled=pharmercy_drug_state.PharmercyDrugState.current_page == 1,
                    ),
                    rx.text(f"Page {pharmercy_drug_state.PharmercyDrugState.current_page} of {pharmercy_drug_state.PharmercyDrugState.total_pages}", color="#330099"),
                    rx.button(
                        rx.icon("chevron-right", color="#330099"),
                        on_click=pharmercy_drug_state.PharmercyDrugState.next_page,
                        variant="ghost",
                        disabled=pharmercy_drug_state.PharmercyDrugState.current_page >= pharmercy_drug_state.PharmercyDrugState.total_pages,
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
        on_mount=pharmercy_drug_state.PharmercyDrugState.on_mount,
    )

def create_drug_dialog():
    """Dialog for creating/editing Drugs."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("plus", size=16),
                    rx.text("Add New Drug"),
                    spacing="2",
                ),
                on_click=pharmercy_drug_state.PharmercyDrugState.open_dialog(None),
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
                    pharmercy_drug_state.PharmercyDrugState.is_editing,
                    "Edit Drug",
                    "Create New Drug"
                )
            ),
            rx.dialog.description(
                "Fill in the details for the drug",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Drug Name",
                    width="100%",
                    value=pharmercy_drug_state.PharmercyDrugState.drug_name,
                    on_change=pharmercy_drug_state.PharmercyDrugState.set_drug_name,
                ),

                rx.input(
                    placeholder="Drug Quantity",
                    type="number",
                    width="100%",
                    value=pharmercy_drug_state.PharmercyDrugState.stock_level,
                    on_change=pharmercy_drug_state.PharmercyDrugState.set_stock_level,
                ),
                rx.text_area(
                    placeholder="Drug Descriptions",
                    width="100%",
                    value=pharmercy_drug_state.PharmercyDrugState.drug_descriptions,
                    on_change=pharmercy_drug_state.PharmercyDrugState.set_drug_description,
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=pharmercy_drug_state.PharmercyDrugState.close_dialog,
                        variant="soft",
                    ),
                    rx.button(
                        rx.cond(
                            pharmercy_drug_state.PharmercyDrugState.is_editing,
                            rx.cond(
                                pharmercy_drug_state.PharmercyDrugState.create_drug,
                                rx.spinner(size="2", color="white"),
                                "Update Drug"
                            ),
                            rx.cond(
                                pharmercy_drug_state.PharmercyDrugState.create_drug,
                                rx.spinner(size="2", color="white"),
                                "Save Drug"
                            ),
                            
                        ),
                        on_click=pharmercy_drug_state.PharmercyDrugState.submit_drug,
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
        open=pharmercy_drug_state.PharmercyDrugState.show_dialog,
    )

def confirm_delete():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(f"Sure to delete {pharmercy_drug_state.PharmercyDrugState.selected_drug["name"]} completely?", text_align="center", margin_y="2rem"),
            rx.hstack(
                rx.button(
                    "Confirm",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=pharmercy_drug_state.PharmercyDrugState.continue_delet_drug,
                ),

                rx.button(
                    "Cancel",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=pharmercy_drug_state.PharmercyDrugState.close_delete_drugs_dialog,
                ),
                justify="center",
                align="center",
                spacing="3",
            ),
            
            padding="2rem",
        ),
        open=pharmercy_drug_state.PharmercyDrugState.is_delete,
    )