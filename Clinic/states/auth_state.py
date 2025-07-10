import reflex as rx
import httpx
from datetime import datetime
from ..services.server_requests import Communicator
# from ..states import admin_state

class UserAuthState(rx.State):
    """Handles authentication logic."""

    is_authenticated: bool = rx.SessionStorage("false") == "true"
    token: str = rx.SessionStorage("")
    username: str = rx.LocalStorage("", sync=True)
    user_id: str = rx.LocalStorage("", sync=True)
    email: str = rx.LocalStorage("", sync=True)
    phone: str = rx.LocalStorage("", sync=True)
    role: str = rx.LocalStorage("", sync=True)

    
    # state management data
    current_date: str = ""
    current_main: str = "Home"
    current_submain: str = "Default"


    # for user login data
    username: str = ""
    password: str = ""
    loading: bool = False

    
    def change_main_view(self, view: str):
        """Change the main view of the landig page"""
        self.current_main = view

    def change_submain_view(self, view):
        """Toggle view for admin login and student login"""
        self.current_submain = view

    def set_username(self, value: str):
        self.username = value.upper()

    def set_password(self, view: str):
        self.password = view

    async def login(self):
        """Handle login and store user data."""
        if self.username == "" or self.password == "":
            yield rx.toast.error("Please fill in all fields", position="top-right")
        
        self.loading = True

        yield
        try:
            response = await Communicator.login(self, self.username, self.password.lower())
            data = response.json()
            if response.status_code == 200 and data.get("access_token"):
                await Communicator.set_token(self, data["access_token"])  # Store token in Communicator for future requests
                self.is_authenticated = True
                self.token = data["access_token"]
                
                self.user_id = data["user_id"]
                self.username = data["username"]
                self.email = data["email"]
                self.phone = data["phone"]
                self.role = data["role"]
                now = datetime.now()
                self.current_date = now.strftime("%d %B, %Y")
                
                if self.role == "doctor":
                    yield rx.redirect("/doctor") 
                
                elif self.role == "pharmacist":
                    yield rx.redirect("/pharmercist")
                
                elif self.role == "lab_attendant":
                    yield rx.redirect("/lab-attendance")
                
                elif self.role == "admin":
                    yield rx.redirect("admin")

                else:
                    yield rx.redirect("/")
            else:
                raise Exception("Invalid credentials")
        except Exception as e:
            print(e)
            yield rx.toast.error(f"Login failed: {str(e)}", position="top-right")
        
        finally:
            self.loading = False
        
        
    
    def logout(self):
        """Clear auth state and redirect."""
        self.token = ""
        self.user_id = ""
        self.email = ""
        self.phone = ""
        self.roles = ""

        yield rx.redirect("/")
    

@staticmethod
def require_auth(page_func):
    """Protect pages from unauthenticated access."""
    def wrapper(*args, **kwargs):
        return rx.cond(
            UserAuthState.is_authenticated,
            page_func(*args, **kwargs),
            rx.fragment(rx.script("window.location.href = '/'"))
        )
    wrapper.__name__ = page_func.__name__  # Preserve the original function name
    return wrapper


