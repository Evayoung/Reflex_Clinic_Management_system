import reflex as rx
from ..states import doctor_state, auth_state
from ..components import doctor_side_bar, footer
from ..services.server_requests import Communicator



class StudentState(rx.State):
    navigator: str = "Dashboard"
    token: str = ""
    show_visit: bool = False
    current_view: str = "Dashboard"
    current_vist_view: str = "Visit List"
    student_info: dict = {}
    appointments: list = []
    messages: list = []

    is_logout: bool = False
    # List of doctors (replace with your actual data)
    # Dialog control
    

    def change_student_view(self, view: str):
        self.current_view = view
        self.navigator = view
        if view == "Visits":
            self.show_visit = True
            self.current_vist_view = "Visit List"
            self.navigator = f"Visits / Visit List"
        else:
            self.show_visit = False

    def change_visit_view(self, view: str):
        self.current_vist_view = view
        self.navigator = f"Visits / {view}"
    

    def logout(self):
        self.is_logout = True

    def cancel_logout(self):
        self.is_logout = False

    def confirm_logout(self):
        self.cancel_logout()
        return rx.redirect("/")
    