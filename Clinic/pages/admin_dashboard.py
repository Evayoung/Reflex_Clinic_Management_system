import reflex as rx
from ..states import auth_state, admin_state

def dashboard_page():
    return rx.center(
        rx.vstack(
            # rx.text(f"Dashboard", font_size="14px", color="#330099"),
            rx.hstack(
                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{admin_state.AdminState.dashboard_data["total_students"]}",),
                            rx.text(f"Registered Students", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),
                        

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="23%",
                    spacing="2",
                    background_color="#ff6600",
                    border_radius="5px",
                ),

                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{admin_state.AdminState.dashboard_data["total_users"]}",),
                            rx.text(f"Registered Staffs", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="23%",
                    spacing="2",
                    background_color="#6699ff",
                    border_radius="5px",
                ),

                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{admin_state.AdminState.dashboard_data["total_doctors"]}",),
                            rx.text(f"Available Doctors", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="23%",
                    spacing="2",
                    background_color="#339966",
                    border_radius="5px",
                ),

                rx.vstack(
                    rx.vstack(
                            rx.heading(f"{admin_state.AdminState.dashboard_data["total_available_drugs"]}",),
                            rx.text(f"Available Drugs", font_size="14px"),
                            padding="1rem",
                            spacing="1",
                            align="center"
                        ),

                    rx.hstack(
                        rx.text(f"More info", font_size="14px", ),
                        rx.icon("circle-arrow-right", size=14), 
                        position="relative",
                        align="center",
                        justify="center",
                        overflow="hidden",
                        width="70%",
                        height="40px",
                        background_color="rgba(0, 0, 0, 0.1)",
                        margin_bottom="15px",
                        border_radius="30px",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease-in-out",
                            "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                        },
                        
                    ),
                        
                    align="center",
                    justify="end",
                    min_width="170px",
                    height="150px",
                    width="23%",
                    spacing="2",
                    background_color="#660287",
                    border_radius="5px",
                ),

                width="100%",
                align="center",
                justify="between",
            ),
            
            rx.hstack(
                rx.vstack(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("#", ),
                                rx.table.column_header_cell("Session", align="center"),
                                rx.table.column_header_cell("Action", align="center"),
                            ),

                            background_color="#330099",
                            color="white",
                            role="grid",
                            padding_left=".25rem",
                        ),
                        
                        rx.table.body(
                            rx.foreach(
                                admin_state.AdminState.paginated_session,
                                lambda w, idx: rx.table.row(
                                    rx.table.cell(rx.cond(w["session_id"], idx+1, "N/A")),
                                    rx.table.cell(rx.cond(w["session_name"], f"{w['session_name']}", "N/A"), align="center"),
                                    rx.table.cell(rx.cond(w["session_id"], 
                                                        rx.hstack(
                                                            rx.vstack(),
                                                            rx.button(
                                                                rx.icon("user-pen", size=16),
                                                                "Edit", 
                                                                bg="green", 
                                                                on_click=admin_state.AdminState.edit_session(w["session_name"]),
                                                                width="100px",
                                                                border_radius="25px",
                                                                ),

                                                            spacing="4",
                                                            align="center",
                                                            justify="center",
                                                            width="100%",
                                                            padding_left="1rem",
                                                            ), 

                                            ),
                                            align="center",
                                        ),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",  
                                            "#ffffff",  # White for odd rows
                                        ),
                                        "color": "#333300",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                ),
                            ),
                        ),
                        variant="ghost",
                        width="100%",
                        # min_height="250px",
                    ),
                    
                    rx.hstack(
                        rx.hstack(
                            rx.hstack(
                                rx.icon("plus", size=16, font_weight="bold"),
                                rx.text("Create Session", font_size="14px"),
                                padding_y=".4rem",
                                padding_x=".9rem",
                                spacing="2",
                                color="white", 
                                align="center",
                                justify="center",
                                cursor="pointer",
                                border_radius="5px",
                                background_image="linear-gradient(45deg, #330099, #4d4dff)",
                                on_click=admin_state.AdminState.open_dialog("session"),
                                _hover={
                                    "transform": "translateY(-2px)",
                                    "transition": "all 0.2s ease-in-out"
                                },
                            ),
                            
                            spacing="4",
                            width="100%",
                            align="center",
                            justify="start",
                        ),
                        rx.hstack(
                            rx.button(
                                "Previous", 
                                on_click=admin_state.AdminState.prev_page, 
                                disabled=admin_state.AdminState.current_session_page == 1, 
                                background_color="transparent",
                                border="2px solid #330099",
                                border_radius="4px 0 0 4px",
                                cursor="pointer",
                                width="120px",
                                height="40px",
                                color="#330099",
                                ),
                            rx.vstack(
                                rx.text(
                                    f"{admin_state.AdminState.current_session_page}", 
                                    color="white", 
                                    font_size="16px", 
                                    font_weight="bold", 
                                    text_align="center"
                                ),
                                
                                width="40px", 
                                height="40px", 
                                align="center",
                                justify="center",
                                background_color="#330099", 
                            ),

                            rx.button(
                                "Next",
                                on_click=admin_state.AdminState.next_page,
                                disabled=(admin_state.AdminState.current_session_page * admin_state.AdminState.items_per_page) >= admin_state.AdminState.session_length,
                                background_color="transparent",
                                border="2px solid #330099",
                                border_radius="0 4px 4px 0",
                                cursor="pointer",
                                width="120px",
                                height="40px",
                                color="#330099",
                            ),
                            spacing="0",
                            justify="end",
                            width="100%",
                            #margin_top="1rem",
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    width="50%",
                    # bg="orange",
                    padding="1rem",
                ),

                rx.vstack(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("#", width="70px"),
                                rx.table.column_header_cell("Level"),
                                rx.table.column_header_cell("Action"),
                            ),

                            background_color="#330099",
                            color="white",
                            font_size="14px",
                            role="grid",
                        ),

                        rx.table.body(
                            rx.foreach(
                                admin_state.AdminState.paginated_level,
                                lambda w, idx: rx.table.row(
                                    rx.table.cell(rx.cond(w["level_id"], idx+1, "N/A")),
                                    rx.table.cell(rx.cond(w["level_name"], f"{w['level_name']}", "N/A"), align="center"),
                                    rx.table.cell(rx.cond(w["level_id"], 
                                                        rx.hstack(
                                                            rx.vstack(),
                                                            rx.button(
                                                                rx.icon("user-pen", size=16),
                                                                "Edit", 
                                                                bg="green", 
                                                                on_click=admin_state.AdminState.edit_level(w["level_name"]),
                                                                width="100px",
                                                                border_radius="25px",
                                                                ),

                                                            spacing="4",
                                                            align="center",
                                                            justify="center",
                                                            width="100%",
                                                            padding_left="1rem",
                                                            ), 

                                            ),
                                            align="center",
                                        ),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",  
                                            "#ffffff",  # White for odd rows
                                        ),
                                        "color": "#333300",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                ),
                            ),
                        ),
                        variant="ghost",
                        width="100%",
                        # min_height="250px",
                    ),

                    rx.hstack(
                        rx.hstack(
                            rx.icon("plus", size=16, font_weight="bold"),
                            rx.text("Create Level", font_size="14px"),
                            padding_y=".4rem",
                            padding_x=".9rem",
                            spacing="2",
                            color="white", 
                            align="center",
                            justify="center",
                            cursor="pointer",
                            border_radius="5px",
                            background_image="linear-gradient(45deg, #330099, #4d4dff)",
                            on_click=admin_state.AdminState.open_dialog("level"),
                            _hover={
                                "transform": "translateY(-2px)",
                                "transition": "all 0.2s ease-in-out"
                            },
                        ),
                        
                        spacing="4",
                        width="100%",
                        align="center",
                        justify="start",
                    ),
                    
                    width="50%",
                    # bg="orange",
                    padding="1rem",
                ),

                spacing="4",
                # align="center",
                width="100%",
            ),
            align="center",
            width="100%",
            spacing="3",
            border_radius="10px",
        ),
        create_session(),
        create_level(),
        border_radius="10px",
        padding="1rem",
        width="100%",
        on_mount=admin_state.AdminState.on_mount,
    )

def create_session():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Create New Session", color="black", magin_bottom="2rem", font_size="23px",),
            rx.vstack(
                rx.hstack(
                    rx.text("Session Name", color="#333300",  font_size="16px", text_align="right", width="180px"),
                    rx.input(
                        placeholder="Enter session Name", 
                        value=admin_state.AdminState.session,
                        on_change=admin_state.AdminState.set_session,
                        width="100%", 
                        height="40px", 
                        required=True,
                        color="#330099",
                        border_radius="0",
                        border="none", 
                        color_scheme="purple",
                        style={"_placeholder": {
                                "color": "#330099",
                                "font_weight": "500"
                            }}, 
                    ),
                    width="100%",
                    align="center",
                ),

                rx.cond(admin_state.AdminState.session_response, rx.text(f"{admin_state.AdminState.session_response}", color="#333300",  font_size="14px", text_align="center", width="100%")),
                spacing="4",
                padding="2rem",
                columns="2",

            ),
            
            rx.hstack(
                rx.button(
                    "Close",
                    bg="transparent",
                    color="#330099",
                    width="120px",
                    height="35px",
                    padding_x="1rem",
                    _hover={"color": "#4d4dff"},
                    on_click=admin_state.AdminState.close_dialog("session"),
                ),

                rx.button(
                    rx.cond(
                        admin_state.AdminState.create_session,
                        rx.spinner(size="2", color="white"),
                        rx.text("Save")
                    ),
                    
                    bg="#330099",
                    color="white",
                    width="120px",
                    height="35px",
                    padding_x="1rem",
                    _hover={"bg": "#4d4dff"},
                    on_click=admin_state.AdminState.save_session,
                ),
                justify="end",
                padding="1rem",
                spacing="4"
            ),
            padding="2rem",
            bg="#ffffff",
        ),
        open=admin_state.AdminState.is_session,
    )


def create_level():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Create New Level", color="black", magin_bottom="2rem", font_size="23px",),
            rx.vstack(
                rx.hstack(
                    rx.text("Level Title", color="#333300",  font_size="16px", text_align="right", width="180px"),
                    rx.input(
                        placeholder="Enter level title", 
                        value=admin_state.AdminState.level,
                        on_change=admin_state.AdminState.set_level,
                        width="100%", 
                        height="40px", 
                        required=True,
                        color="#330099",
                        border_radius="0",
                        border="none", 
                        color_scheme="purple",
                        style={"_placeholder": {
                                "color": "#330099",
                                "font_weight": "500"
                            }}, 
                    ),
                    width="100%",
                    align="center",
                ),

                rx.cond(admin_state.AdminState.level_response, rx.text(f"{admin_state.AdminState.level_response}", color="#333300",  font_size="14px", text_align="center", width="100%")),
                spacing="4",
                padding="2rem",
                columns="2",

            ),
            
            rx.hstack(
                rx.button(
                    "Close",
                    bg="transparent",
                    color="#330099",
                    width="120px",
                    height="35px",
                    padding_x="1rem",
                    _hover={"color": "#4d4dff"},
                    on_click=admin_state.AdminState.close_dialog("level"),
                ),

                rx.button(
                    rx.cond(
                        admin_state.AdminState.create_level,
                        rx.spinner(size="2", color="white"),
                        rx.text("Save")
                    ),
                    
                    bg="#330099",
                    color="white",
                    width="120px",
                    height="35px",
                    padding_x="1rem",
                    _hover={"bg": "#4d4dff"},
                    on_click=admin_state.AdminState.save_levels,
                ),
                justify="end",
                padding="1rem",
                spacing="4"
            ),
            padding="2rem",
            bg="#ffffff",
        ),
        open=admin_state.AdminState.is_level,
    )