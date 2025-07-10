import reflex as rx
from ..states import auth_state, admin_state

def user_page():
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Clinic User Lists",
                    size="6",
                    color="#333300",
                    text_align="left",
                ),
                rx.hstack(
                    rx.icon("plus", size=16, font_weight="bold"),
                    rx.text("Create User", font_size="14px"),
                    padding_y=".4rem",
                    padding_x=".9rem",
                    spacing="2",
                    color="white", 
                    align="center",
                    justify="center",
                    cursor="pointer",
                    border_radius="5px",
                    background_image="linear-gradient(45deg, #330099, #4d4dff)",
                    on_click=admin_state.AdminState.open_user_dialog('create_new'),
                    _hover={
                        "transform": "translateY(-2px)",
                        "transition": "all 0.2s ease-in-out"
                    },
                ),
                
                spacing="4",
                width="100%",
                align="center",
                justify="between",
            ),
            rx.grid(
                rx.foreach(
                    admin_state.AdminState.users,
                    lambda user: users_card(user["username"], user["role"], user["user_id"])
                ),
                columns="1",
                spacing="3",
                width="100%",
                padding="1rem",
                max_height="70vh",
                overflow_y="auto",
            ),

            align="center",
            width="100%",
            spacing="3",
            border_radius="10px",
        ),
        create_user(),
        view_user(),
        border_radius="10px",
        padding="1rem",
        width="100%",
        # on_mount=admin_state.AdminState.on_mount,
    )


def users_card(name: str, user_role: str, user_id: str):
    return rx.card(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src="/user_pics.png",
                    width="60px",
                    height="auto",
                    border_radius="8px",
                ),

                rx.vstack(
                    rx.heading(name, size="4", color="#330099"),
                    rx.text(f"{user_role}", color="#666633", font_size="12px"),
                    spacing="1"
                ),
                width="100%",
                spacing="4"
            ),
            rx.button(
                "View",
                on_click=admin_state.AdminState.view_user_dialog(user_id),
                bg="#330099",
                color="white",
                _hover={"bg": "#3555A0"},
                width="90px",
            ),
            rx.button(
                "Edit",
                on_click=admin_state.AdminState.edit_users(user_id),
                bg="#330099",
                color="white",
                _hover={"bg": "#544BC7"},
                width="90px",
            ),
            spacing="2",
            align="center",
            justify="between",
            width="100%"
        ),
        
        width="100%",
        padding="1rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def create_user():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add New user", color="black", magin_bottom="2rem", font_size="23px",),
            rx.vstack(
                rx.hstack(
                    rx.text("First Name:", color="#333300",  font_size="16px", text_align="left", width="130px"),
                    rx.input(
                        placeholder="Enter user name..", 
                        value=admin_state.AdminState.username,
                        on_change=admin_state.AdminState.change_username,
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

                rx.hstack(
                    rx.text("Surname:", color="#333300",  font_size="16px", text_align="left", width="130px"),
                    rx.input(
                        placeholder="Enter user surname..", 
                        value=admin_state.AdminState.surname,
                        on_change=admin_state.AdminState.change_surname,
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

                rx.hstack(
                    rx.text("Password:", color="#333300",  font_size="16px", text_align="left", width="130px"),
                    rx.input(
                        placeholder="Enter password for user", 
                        value=admin_state.AdminState.password,
                        on_change=admin_state.AdminState.change_password,
                        width="100%", 
                        height="40px",
                        color_scheme="purple",  
                        required=True,
                        border_radius="0",
                        border="none", 
                        color="#330099", 
                    ),
                    width="100%",
                    align="center",
                ),
                
                rx.hstack(
                    rx.text("User Type:", color="#333300",  font_size="16px", text_align="left", width="200px"),
                    rx.select(
                        admin_state.AdminState.roles,
                        placeholder="Select Recipient Type",
                        value=admin_state.AdminState.role,
                        on_change=admin_state.AdminState.change_role,
                        width="76%",
                        height="40px",
                        color="white",
                        bg="white",
                        variant="classic",
                        border_color="#333300",
                        _hover={"border_color": "#4d4d33"},
                    ),
                    width="100%",
                    align="center",
                ),

                rx.hstack(
                    rx.text("User Email", color="#333300",  font_size="16px", text_align="left", width="130px"),
                    rx.input(
                        placeholder="Enter user email", 
                        value=admin_state.AdminState.email,
                        on_change=admin_state.AdminState.change_email,
                        width="100%", 
                        height="40px",
                        color_scheme="purple",  
                        required=True,
                        border_radius="0",
                        border="none", 
                        color="#330099", 
                    ),
                    width="100%",
                    align="center",
                ),

                rx.hstack(
                    rx.text("User phone:", color="#333300",  font_size="16px", text_align="left", width="130px"),
                    rx.input(
                        placeholder="Enter user phone:", 
                        value=admin_state.AdminState.phone,
                        on_change=admin_state.AdminState.change_phone,
                        type="password",
                        width="100%", 
                        height="40px",
                        color_scheme="purple",  
                        required=True,
                        border_radius="0",
                        border="none", 
                        color="#330099", 
                    ),
                    width="100%",
                    align="center",
                ),

                rx.hstack(
                    rx.text("User status:", color="#333300",  font_size="16px", text_align="left", width="200px"),
                    rx.select(
                        admin_state.AdminState.status_type,
                        placeholder="Select user status",
                        value=admin_state.AdminState.status,
                        on_change=admin_state.AdminState.change_status,
                        width="76%",
                        height="40px",
                        color="white",
                        bg="white",
                        variant="classic",
                        border_color="#333300",
                        _hover={"border_color": "#4d4d33"},
                    ),
                    width="100%",
                    align="center",
                ),

                rx.cond(admin_state.AdminState.user_response, rx.text(f"{admin_state.AdminState.user_response}", color="#333300",  font_size="14px", text_align="center", width="100%")),
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
                    on_click=admin_state.AdminState.close_user_dialog,
                ),

                rx.button(
                    rx.cond(
                        admin_state.AdminState.create_user,
                        rx.spinner(size="2", color="white"),
                        rx.text("Save")
                    ),
                    
                    bg="#330099",
                    color="white",
                    width="120px",
                    height="35px",
                    padding_x="1rem",
                    _hover={"bg": "#4d4dff"},
                    on_click=admin_state.AdminState.save_user,
                ),
                justify="end",
                padding="1rem",
                spacing="4"
            ),
            padding="2rem",
            bg="#ffffff",
        ),
        open=admin_state.AdminState.is_user,
    )


def view_user():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("User Profile", color="black", magin_bottom="2rem", font_size="23px",),
            rx.vstack(
                rx.vstack(
                    rx.image(
                        src="/user_pics.png",
                        width="120px",
                        height="auto",
                        border_radius="8px",
                    ),
                    rx.vstack(
                        rx.heading(admin_state.AdminState.selected_user_name, size="4", color="#333300"),
                        rx.text(f"{admin_state.AdminState.selected_user_id}", color="#666633", font_size="15px"),
                        spacing="1",
                        width="100%",
                        align="center"
                    ),

                    width="100%",
                    align="center",
                    justify="center",
                    spacing="4"
                ),
                rx.data_list.root(
                        rx.data_list.item(
                            rx.data_list.label("User Type:", color="#333300", text_align="right"),
                            rx.data_list.value(
                                rx.text(f"{admin_state.AdminState.selected_user_role}", color="#666633", font_size="16px"),
                            ),
                            spacing="4",
                            justify="center",
                        ),
                        rx.data_list.item(
                            rx.data_list.label("Phone Number:", color="#333300", text_align="right"),
                            rx.data_list.value(
                                rx.text(f"{admin_state.AdminState.selected_user_phone}", color="#666633", font_size="16px"),
                            ),
                            spacing="4",
                            justify="center",
                        ),
                        rx.data_list.item(
                            rx.data_list.label("Email:", color="#333300", text_align="right"),
                            rx.data_list.value(
                                rx.text(f"{admin_state.AdminState.selected_user_email}", color="#666633", font_size="16px"),
                            ),
                            spacing="4",
                            justify="center",
                        ),
                        rx.data_list.item(
                            rx.data_list.label("Status:", color="#333300", text_align="right"),
                            rx.data_list.value(
                                rx.text(f"{admin_state.AdminState.selected_user_status}", color="#666633", font_size="16px"),
                            ),
                            spacing="4",
                            justify="center",
                        ),
                    
                    align="center",
                ),

                spacing="4",
                padding="2rem",
                columns="2",
                justify="center",

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
                    on_click=admin_state.AdminState.close_dialog('user'),
                ),
                justify="end",
                padding="1rem",
                spacing="4"
            ),
            padding="2rem",
            bg="#ffffff",
        ),
            
        open=admin_state.AdminState.view_user,
    )