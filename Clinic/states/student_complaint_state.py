import reflex as rx
from datetime import datetime
from ..services.server_requests import Communicator


class StudentComplaintState(rx.State):
    """State for managing student complaint page"""
    loading: bool = False
    is_sumbmit: bool = False
    schedule_options: list[str] = []
    selected_schedule: int = 0
    complaint_description: str = ""
    visits: list[dict] = []
    token: str = ""

    selected_visit: dict = {}
    show_visit_detail: bool = False


    # card data
    card_data: dict = {}
    student_data: dict = {}
    student_info: dict = {}
    complaints: list[dict] = []
    picture: str = ""

    session: str = ""
    level: str = ""
    clinic_number: str = ""
    issue_date: str = ""
    expiry_date: str = ""
    blood_group: str = ""
    genotype: str = ""
    height: float = 0.0
    weight: float = 0.0
    test_date: str = ""
    

    show_dialog: bool = False
    selected_schedule_str: str = ""

    student_compalints: dict = {}
    diagnosis: dict = {}
    prescriptions: list[dict] = []

    student_health: dict = {}

    dashboard_data: dict = {}
    doctors: list[dict] = []
    total_doctors: str = ""

    show_doctor_dialog: bool = False
    selected_doctor: dict = {}
    
    def open_doctor_dialog(self, doctor: dict):
        """Open dialog with selected doctor's data"""
        self.selected_doctor = doctor
        self.show_doctor_dialog = True
    
    def close_doctor_dialog(self):
        """Close the dialog"""
        self.show_doctor_dialog = False




    async def on_mount(self, data: dict):
        self.student_info = data
        
        profile, visits, schedules, dashboard = await Communicator.get_student_details(self, data["access_token"])

        self.schedule_options = [
            f"{s['schedule_id']} | {s['doctor_name']} | {s['date']} {s['start_time']} - {s['end_time']}"
            for s in schedules.json()
        ]
        self.visits = visits.json() if visits.status_code == 200 else []
        self.dashboard_data = dashboard.json() if dashboard.status_code == 200 else {}
        self.doctors = [doctors for doctors in self.dashboard_data["active_doctors"]]
        self.total_doctors = str(len(self.doctors))
        
        self.student_data = profile.json() if profile.status_code == 200 else {}
        self.picture = f"{'http://localhost:8006'}/{self.student_data['profile_picture']}"
        self.clinic_number = self.student_data["latest_clinic_card"]["clinic_number"]
        self.issue_date = self.student_data["latest_clinic_card"]["issue_date"]
        self.expiry_date = self.student_data["latest_clinic_card"]["expiry_date"]
        self.student_health = self.student_data["latest_health_record"]


    def set_selected_schedule(self, value: str):
        self.selected_schedule = int(value.split("|")[0].strip())

    def set_complaint_description(self, value: str):
        self.complaint_description = value

    async def submit_complaint(self):
        if not self.selected_schedule or not self.complaint_description:
            yield rx.toast.error("Please select a schedule and enter a complaint.", position="top-right")
            return

        self.is_sumbmit = True
        yield
        try:
            payload = {
                "schedule_id": self.selected_schedule,
                "complaint_description": self.complaint_description,
            }

            result = await Communicator.submit_complaint(payload, self.student_info["access_token"])
            if result.status_code == 201:
                print(result.json())
                self.visits.append(result.json()) # append data from response
                rx.toast.success("Complaint submitted successfully.", position="top-right")
                self.complaint_description = ""
                self.selected_schedule = 0
            else:
                rx.toast.error(f"Failed to submit complaint: {result}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            yield rx.toast.error("An unexpected error occurred. Please try again.",  position="top-right")
        finally:
            self.is_sumbmit = False
            

            
    async def view_visit(self, visit_id: int):
        try:
            self.show_visit_detail = False
            token = self.student_info["access_token"]
            result = await Communicator.get_full_visits(token, visit_id)
            if result.status_code == 200:
                self.selected_visit = result.json()
                self.show_visit_detail = True
                self.student_compalints = self.selected_visit["complaint"]
                self.diagnosis = self.selected_visit["diagnosis"]
                self.prescriptions = [presc for presc in self.selected_visit["prescriptions"]]
            else:
                yield rx.toast.error("Could not retrieve visit details.", position="top-right")
        except Exception as e:
            print(f"Visit view error: {e}")
            yield rx.toast.error("An unexpected error occurred while fetching visit.", position="top-right")


    def close_visit_detail(self):
        self.show_visit_detail = False
        self.selected_visit = {}

    def open_dialog(self):
        self.show_dialog = True

    def close_dialog(self):
        self.show_dialog = False
        self.complaint_description = ""
        self.selected_schedule_str = ""

    def set_selected_schedule(self, value: str):
        self.selected_schedule_str = value
        self.selected_schedule = int(value.split("|")[0].strip()) if "|" in value else 0
