import reflex as rx
from ..components import navbar, footer, signin, staff_signin, sign_up
from ..states.auth_state import UserAuthState

def landing_page():
    return rx.flex(

        rx.cond(
            UserAuthState.current_submain == "Default",
                  # Default landing page
            rx.vstack(
                rx.text("CLINIC MANAGEMENT SYSTEM", font_size="2.5rem", font_weight="bold"),
                rx.text("""Welcome to the University of Ilorin Clinic Management System, your one-stop 
                        platform for seamless healthcare services. Easily book appointments, access digital 
                            clinic cards, and manage health records as a student or staff member.""", 
                        font_size="1.1rem", text_align="center", width="70%"),

                rx.hstack(
                    rx.button(
                        "Staff Login",
                        # Base styling
                        padding="1.5rem 2.5rem",
                        border_radius="8px",
                        font_weight="400",
                        font_size="1rem",
                        color="#e67e22",
                        bg="white",  
                        transition="all 0.3s ease",
                        position="relative",
                        overflow="hidden",
                        on_click=UserAuthState.change_submain_view("Staff"),
                        _before={
                            "content": '""',
                            "position": "absolute",
                            "width": "0%",
                            "height": "100%",
                            "top": "0",
                            "left": "0",
                            "background": "#e67e22",
                            "transition": "all 0.3s ease",
                            "z_index": "-1",
                        },
                        # Hover effects
                        _hover={
                            "color": "white",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                            "_before": {
                                "width": "100%",
                            }
                        },
                        # Active/pressed effect
                        _active={
                            "transform": "translateY(0)",
                            "box_shadow": "none"
                        },
                    ),

                    rx.button(
                        "Student Login",
                        # Base styling
                        padding="1.5rem 2.5rem",
                        border_radius="8px",
                        font_weight="400",
                        font_size="1rem",
                        color="#e67e22",
                        bg="white",  
                        transition="all 0.3s ease",
                        position="relative",
                        overflow="hidden",
                        on_click=UserAuthState.change_submain_view("Student"),
                        _before={
                            "content": '""',
                            "position": "absolute",
                            "width": "0%",
                            "height": "100%",
                            "top": "0",
                            "left": "0",
                            "background": "#e67e22",
                            "transition": "all 0.3s ease",
                            "z_index": "-1",
                        },
                        # Hover effects
                        _hover={
                            "color": "white",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                            "_before": {
                                "width": "100%",
                            }
                        },
                        # Active/pressed effect
                        _active={
                            "transform": "translateY(0)",
                            "box_shadow": "none"
                        },
                    ),
                    width="100%",
                    justify="center",
                    spacing="8",
                    align="center",
                ),

                # width="70%",
                padding="2rem",
                justify="center",
                align="center",
                color="white",
                spacing="6"
            ),
        
            rx.cond(
                UserAuthState.current_submain=="Staff",
                staff_signin.sign_in(),
                rx.cond(
                    UserAuthState.current_submain=="Student",
                    signin.sign_in(),
                    rx.cond(
                        UserAuthState.current_submain=="Create Student",
                        sign_up.sign_up(),
                    ),
                ),
            ),
        ),
        
    
        # Staffs login page
        rx.vstack(

        ),

        # Student login page
        rx.vstack(

        ),

        spacing="8",
        direction="column",
        align="center",
        justify="center",
        wrap="wrap",
        width="100%",
        padding="4",
    )


def news_page():
    return rx.flex(
        
        rx.vstack(
            rx.text("Trending News!", font_size="2.5rem", font_weight="bold"),
            rx.text("""Welcome to the University of Ilorin Clinic Management System, your one-stop 
                    platform for seamless healthcare services. Easily book appointments, access digital 
                        clinic cards, and manage health records as a student or staff member.""", 
                    font_size="1.1rem", text_align="center", width="70%"),

            rx.hstack(
                rx.button(
                    "Visit School Portal",
                    # Base styling
                    padding="1.5rem 2.5rem",
                    border_radius="8px",
                    font_weight="400",
                    font_size="1rem",
                    color="#e67e22",
                    bg="white",  
                    transition="all 0.3s ease",
                    position="relative",
                    overflow="hidden",
                    _before={
                        "content": '""',
                        "position": "absolute",
                        "width": "0%",
                        "height": "100%",
                        "top": "0",
                        "left": "0",
                        "background": "#e67e22",
                        "transition": "all 0.3s ease",
                        "z_index": "-1",
                    },
                    # Hover effects
                    _hover={
                        "color": "white",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                        "_before": {
                            "width": "100%",
                        }
                    },
                    # Active/pressed effect
                    _active={
                        "transform": "translateY(0)",
                        "box_shadow": "none"
                    },
                ),

                width="100%",
                justify="center",
                spacing="8",
                align="center",
            ),

            # width="70%",
            padding="2rem",
            justify="center",
            align="center",
            color="white",
            spacing="6"
        ),
        
        spacing="8",
        direction="column",
        align="center",
        justify="center",
        wrap="wrap",
        width="100%",
        padding="4",
    )


def about_page():
    return rx.flex(
        
        rx.vstack(
            rx.text("Welcome Here!", font_size="2.5rem", font_weight="bold"),
            rx.text("""Welcome to the University of Ilorin Clinic Management System, your one-stop 
                    platform for seamless healthcare services. Easily book appointments, access digital 
                        clinic cards, and manage health records as a student or staff member.""", 
                    font_size="1.1rem", text_align="center", width="70%"),

            
            # width="70%",
            padding="2rem",
            justify="center",
            align="center",
            color="white",
            spacing="6"
        ),
        
        spacing="8",
        direction="column",
        align="center",
        justify="center",
        wrap="wrap",
        width="100%",
        padding="4",
    )


def index() -> rx.Component:
    return rx.box(
        navbar.index_nav(),

        # Main content
        rx.box(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.image(
                                src="/clinic_bg.jpg",
                                height="100%",
                                width="100%",
                                object_fit="cover",
                                position="absolute",
                                # border_radius="1.5em",
                                z_index="0",
                            ),
                            # Overlay
                            rx.box(
                                height="100%",
                                width="100%",
                                position="absolute",
                                bg="rgba(0, 0, 0, 0.6)",
                                z_index="0",
                                # border_radius="1.5em",
                            ),
                            rx.center(
                                rx.mobile_and_tablet(
                                    rx.text(
                                        "This App is designed to work better on a desktop environment, please switch to a desktop machine",
                                        font_size="1.5rem",
                                        font_weight="400",
                                        color="white",
                                        text_align="center",
                                    ),
                                ),
                                rx.desktop_only(
                                    rx.cond(
                                        UserAuthState.current_main == "Home",
                                        landing_page(),
                                        rx.cond(
                                            UserAuthState.current_main == "News",
                                            news_page(),
                                            rx.cond(
                                                UserAuthState.current_main == "About",
                                                about_page(),
                                                
                                            ),
                                        ),
                                    ),
                                    
                                ),
                                
                                width="100%",
                                height="100%",
                                # padding=rx.breakpoints(initial="1rem", sm="2rem"),
                                z_index="1",
                                position="absolute",
                            ),
                            height="100vh",
                            width="100%",
                            # position="relative",
                            border_radius="0 0 2em 2em",  # Curved bottom border
                        ),
                        
                        spacing="6",  # Add space between the sections
                        width="100%",
                    ),
                    width="100%",
                    overflow_y="auto",  # Enable scrolling
                    max_height="calc(100vh - 70px)",  # Adjust height dynamically
                    # padding_right=".4rem", 
                ),
            ),

            # padding_x="2rem",  # Consistent horizontal padding
            # margin_top="70px",  # Adjust based on navbar height
            width="100%",
            background_color="#ffffff",
            overflow="hidden",
        ),
        footer.footer(),
        background_color="#ffffff",
    )
