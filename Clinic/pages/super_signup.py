import reflex as rx
import httpx
from typing import Optional
from datetime import datetime
from ..services.server_requests import Communicator
BACKEND_URL = "http://localhost:8006"

class SuperAdminFormState(rx.State):
    """State for the super admin creation form."""
    name: str = ""
    email: str = ""
    phone: str = ""
    password: str = ""
    confirm_password: str = ""
    is_loading: bool = False
    error_message: str = ""
    show_success_dialog: bool = False
    created_admin: Optional[dict] = None

    # State setters
    def set_name(self, name: str):
        """Set the name field value."""
        self.name = name

    def set_email(self, email: str):
        """Set the email field value."""
        self.email = email

    def set_phone(self, phone: str):
        """Set the phone field value."""
        self.phone = phone

    def set_password(self, password: str):
        """Set the password field value."""
        self.password = password

    def set_confirm_password(self, confirm_password: str):
        """Set the confirm password field value."""
        self.confirm_password = confirm_password

    def set_show_success_dialog(self, show: bool):
        """Set the success dialog visibility."""
        self.show_success_dialog = show

    def reset_form(self):
        """Reset the form fields."""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.password = ""
        self.confirm_password = ""
        self.error_message = ""
        self.is_loading = False

    def validate_inputs(self) -> bool:
        """Validate form inputs."""
        if not self.name or not self.email or not self.password:
            self.error_message = "All fields are required"
            return False
        
        if "@" not in self.email or "." not in self.email:
            self.error_message = "Please enter a valid email address"
            return False
        
        if self.password != self.confirm_password:
            self.error_message = "Passwords do not match"
            return False
        
        if len(self.password) < 8:
            self.error_message = "Password must be at least 8 characters"
            return False
        
        return True


    def process_response(self, response):
        """Process the API response."""
        if response.status_code == 201:
            response_data = response.json()
            self.created_admin = {
                "admin_id": response_data["user_id"],
                "name": response_data["username"],
                "email": response_data["email"],
                "role": response_data["role"],
                "phone": response_data["phone"]
            }
            self.show_success_dialog = True
            self.reset_form()
        else:
            error_data = response.json()
            self.error_message = error_data.get("detail", "Failed to create Super Admin")

    async def handle_submit(self):
        """Handle form submission."""
        if not self.validate_inputs():
            return

        self.is_loading = True
        self.error_message = ""
        yield
        try:

            payload = {
                "username": self.name,
                "password": self.password,
                "email": self.email,
                "phone": self.phone,  
                "status": "active",  
            }
            # response = await self.submit_admin_data()
            #response = await Communicator.create_user(self, payload)
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BACKEND_URL}/admin/super-admin/signup", json=payload, headers={"Content-Type": "application/json"})
                response.raise_for_status()
            
            # return response
            self.process_response(response)
        except Exception as e:
            self.error_message = f"An error occurred: {str(e)}"
        finally:
            self.is_loading = False

def format_datetime(dt_str: str) -> str:
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return dt_str

def admin_detail_row(label: str, value: str):
    """Create a styled row for admin details."""
    return rx.hstack(
        rx.text(label, width="120px", font_weight="bold"),
        rx.text(value),
        width="100%",
    )

def success_dialog():
    """Dialog showing successful admin creation with details."""
    return rx.dialog.root(
        rx.dialog.trigger(rx.box(display="none")),  # Hidden trigger
        rx.dialog.content(
            rx.dialog.title("Super Admin Created Successfully!"),
            rx.dialog.description(
                rx.vstack(
                    admin_detail_row("Admin ID:", SuperAdminFormState.created_admin["admin_id"]),
                    admin_detail_row("Name:", SuperAdminFormState.created_admin["name"]),
                    admin_detail_row("Email:", SuperAdminFormState.created_admin["email"]),
                    admin_detail_row("Role:", SuperAdminFormState.created_admin["role"]),
                    admin_detail_row("Phone:", SuperAdminFormState.created_admin["phone"]),
                    rx.text("Please copy your user ID for future reference.", font_style="italic"),
                    spacing="3",
                ),
                margin_top="1em",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Close",
                        color_scheme="green",
                    ),
                ),
                justify="end",
                margin_top="1em",
            ),
            style={"max_width": "500px"},
        ),
        open=SuperAdminFormState.show_success_dialog,
        on_open_change=SuperAdminFormState.set_show_success_dialog,
    )

def super_admin_form():
    """Form for creating a super admin."""
    return rx.vstack(
        rx.heading("Create Super Admin", size="6", color="#330099"),
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Full Name",
                    id="name",
                    value=SuperAdminFormState.name,
                    on_change=SuperAdminFormState.set_name,
                    is_required=True,
                    width="100%",
                    variant="surface",
                    color_scheme="purple",
                    color="purple",
                    size="3"
                ),
                rx.input(
                    placeholder="Email",
                    id="email",
                    type_="email",
                    value=SuperAdminFormState.email,
                    on_change=SuperAdminFormState.set_email,
                    is_required=True,
                    width="100%",
                    variant="surface",
                    color_scheme="purple",
                    color="purple",
                    size="3"
                ),
                rx.input(
                    placeholder="Phone Number",
                    id="phone",
                    type_="tel",
                    value=SuperAdminFormState.phone,
                    on_change=SuperAdminFormState.set_phone,
                    is_required=True,
                    width="100%",
                    variant="surface",
                    color_scheme="purple",
                    color="purple",
                    size="3"
                ),
                rx.input(
                    placeholder="Password",
                    id="password",
                    type="password",
                    value=SuperAdminFormState.password,
                    on_change=SuperAdminFormState.set_password,
                    is_required=True,
                    width="100%",
                    variant="surface",
                    color_scheme="purple",
                    color="purple",
                    size="3"
                ),
                rx.input(
                    placeholder="Confirm Password",
                    id="confirm_password",
                    type="password",
                    value=SuperAdminFormState.confirm_password,
                    on_change=SuperAdminFormState.set_confirm_password,
                    is_required=True,
                    width="100%",
                    variant="surface",
                    color_scheme="purple",
                    color="purple",
                    size="3"
                ),
                rx.hstack(
                    rx.link(
                        "< Back to Login",
                        href="/",
                        color="#330099",
                        text_align="center",
                        width="200px",
                        font_size="1rem",
                        font_weight="bold",
                        text_decoration="none",
                        # style={"text_decoration": "none"},
                        _hover={"color": "#5A3D94", "text_decoration": "underline"},
                    ),
                    rx.button(
                        rx.cond(
                            SuperAdminFormState.is_loading,
                            "Creating...",  # Show loading text when loading
                            "Create Account"  # Default button text
                        ),
                        type_="submit",
                        width="45%",
                        color_scheme="purple",
                        height="40px",
                    ),
                    
                    width="100%",
                    padding_x="2rem",
                    padding_y="1rem",
                    align="center",
                ),
                spacing="4",
            ),
            on_submit=SuperAdminFormState.handle_submit,
            width="100%",
        ),
        rx.cond(
            SuperAdminFormState.error_message != "",
            rx.callout(
                SuperAdminFormState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
                width="100%",
            ),
        ),
        width=["100%", "500px"],
        padding="2em",
        spacing="4",  
        height="75%", 
        # min_width="750px", 
        border_radius="2em",  # Curved corners for the vstack
        background_color="#ffffff",
        box_shadow="0 2px 4px rgba(0,0,0,0.5)",
        align="center",  
        justify="center", 
    )

def index():
    """Main page with the super admin form."""
    return rx.center(
        rx.vstack(
            super_admin_form(),
            success_dialog(),
            spacing="4",
        ),
        width="100%",
        height="100vh",
        bg="#f0f0f0",  # Light gray background
    )

# UIL/25/326