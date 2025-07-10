import reflex as rx
from datetime import datetime
from ..services.server_requests import Communicator
from ..states.auth_state import UserAuthState

class PharmercistState(rx.State):
    """Handles authentication logic."""
    
    # state management data
    current_view: str = "Dashboard"
    navigator: str = "Dashboard"
    token: str = ""
    is_logout: bool = False

    session: str = ""
    level: str = ""
    


    def change_pharm_view(self, view: str):
        self.current_view = view
        self.navigator = view

    async def continue_logout(self):
        self.is_logout = False
        yield rx.redirect("/")

    def cancel_logout(self):
        self.is_logout = False

    def logout(self):
        self.is_logout = True