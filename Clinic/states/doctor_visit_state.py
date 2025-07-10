import reflex as rx
import httpx
from ..states import doctor_state, auth_state
from ..services.server_requests import Communicator


class DoctorVisitState(rx.State):
    navigator: str = ""
    token: str = ""
    # current_view: str = "Visit List"
    pending: list[dict] = []
    current_visit: dict = {}
    current_diagnosis: str = ""
    current_treatment_plan: str = ""
    prescriptions: list[dict] = []
    new_prescription: dict = {"drug_id": "", "dosage": "", "instructions": ""}
    available_drugs: list[dict] = []
    drugs: list = []
    health_records: dict = {}

    edit_diagnoses_id: int = 0

    selected_student: dict = {}
    student_visit: dict = {}
    visit_complaint: dict = {}
    visit_diagnosis: dict = {}
    visit_data: dict = {}
    visit_prescription: list[dict] = []

    added_data: dict = {}

    loaded_diagnosis: dict = {}
    loaded_prescription: list[dict] = []

    drug_id: str = ""
    drug: str = ""
    dosage: str = ""
    instruction: str = ""

    diagnosis: str = ""
    treatment: str = ""

    add_diagnosis: bool = False
    is_diagnosis: bool = False
    edit_diagnosis: bool = False
    add_prescriptions: bool = False
    is_prescriptions: bool = False
    edit_prescriptions: bool = False


    # Pagination
    current_page: int = 1
    items_per_page: int = 10
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "10"
    # Search
    search_query: str = ""

    show_visit: bool = False
    current_view: str = "Dashboard"
    current_vist_view: str = "Visit List"

    def set_drug_id(self, value):
        self.drug = value
        self.drug_id = [id["drug_id"] for id in self.available_drugs if id["name"] == value][0]
        print(self.drug_id)
        

    def set_dosage(self, value: str):
        self.dosage = value


    def set_instruction(self, value: str):
        self.instruction = value
        

    def set_current_diagnosis(self, value: str):
        self.current_diagnosis = value

    def set_current_treatment_plan(self, value: str):
        self.current_treatment_plan = value

    def change_doctor_view(self, view: str):
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

    async def get_pending_data(self, data, data2):
        """Set pending visits from parent state"""
        self.pending = data
        self.available_drugs = data2
        print(self.available_drugs)
        self.drugs = [drug["name"] for drug in self.available_drugs]

    async def edit_selected_student(self, visit_id: int):
        self.selected_student = [s for s in self.pending if visit_id == s.get("visit_id", "")][0]
        self.edit_diagnoses_id = visit_id
        self.change_visit_view("Create Visit")
        await self.load_daignoses_prescription(visit_id)
        
        

    async def view_selected_student(self, visit_id: int):
        self.selected_student = [s for s in self.pending if visit_id == s.get("visit_id", "")][0]
        self.change_visit_view("View Visit")
        await self.load_visit_details(visit_id)

    async def load_daignoses_prescription(self, visit_id: int):
        """Load full details for a specific visit"""
        admin = await self.get_state(auth_state.UserAuthState)
        auth = admin.token
        try:
            response = await Communicator.get_visit_diagnoses(auth, visit_id)
            response2 = await Communicator.get_visit_prescription(auth, visit_id)
            if response.status_code != 200:
                rx.toast.error(f"Failed to load visit details: {response.text}", position="top-right")
                return
            else:
                self.loaded_diagnosis = response.json()[0]

            if response2.status_code != 200:
                rx.toast.error(f"Failed to load prescription details: {response2.text}", position="top-right")
                return
            else:
                print(response2.json())
                self.loaded_prescription = response2.json()
            
        except Exception as e:
            print(f"Error loading visit: {e}")


    async def load_visit_details(self, visit_id: int):
        """Load full details for a specific visit"""
        try:
            response = await Communicator.get_student_visit(visit_id)
            if response.status_code != 200:
                rx.toast.error(f"Failed to load visit details: {response.text}", position="top-right")
                return
            
            self.visit_data = response.json()
            self.student_visit = self.visit_data["student"]
            self.visit_complaint = self.visit_data["complaints"]
            self.visit_diagnosis = self.visit_data["diagnosis"]
            self.visit_prescription = [p for p in self.visit_diagnosis["prescriptions"]]
            print(self.visit_prescription)
            
            
        except Exception as e:
            print(f"Error loading visit: {e}")

    async def add_prescription(self):
        """Add prescription to current visit"""
        new_data = {"drug_id": self.drug_id, "dosage": self.dosage, "instructions": self.instruction}
        self.prescriptions.append(new_data)

    def delete_prescription(self, data: dict):
        for i in self.prescriptions:
            if data == i:
                self.prescriptions.remove(i)
            yield rx.toast.success("Prescription removed from list!", position="top-right")
        
        

    def set_search_query(self, value: str):
        self.search_query = value
        self.current_page = 1  

    # ========== Pagination Methods ==========
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
    
    def change_items_per_page(self, value: str):
        """Change items per page"""
        self.items_per_page = int(value)
        self.current_page = 1
        self.show_choice = value
        yield rx.toast.success(f"Items per page set to {value}", position="top-right")    

    # ========== Computed Properties ==========
    @rx.var
    def filtered_appointment(self) -> list[dict]:
        """Filter schedules based on search query"""
        if not self.search_query:
            return self.pending
        return [
            s for s in self.pending 
            if self.search_query.lower() in s.get("student_name", "").lower()
        ]
    
    @rx.var
    def paginated_appointment(self) -> list[dict]:
        """Paginate filtered schedules"""
        start = (self.current_page - 1) * self.items_per_page
        return self.filtered_appointment[start:start+self.items_per_page]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages"""
        return max(1, (len(self.filtered_appointment) + self.items_per_page - 1) // self.items_per_page)


    # Diagnosis section
    # ======================================================================
    def open_diagnosis_dialog(self, diagnosis: dict | None = None):
        """Open dialog for creating/editing diagnosis."""
        if diagnosis:
            self.edit_diagnosis = True
            self.diagnosis = diagnosis["drug_id"]
            self.treatment = diagnosis["name"]
        else:
            self.edit_diagnosis = False
            self.diagnosis = ""
            self.treatment = ""
        self.add_diagnosis = True
    
    def close_diagnosis_dialog(self):
        """Close the dialog."""
        self.add_diagnosis = False


    async def create_diagnosis(self):
        """Submit diagnosis for current visit"""
        if not self.current_diagnosis or not self.current_treatment_plan:
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return
        
        self.is_diagnosis = True
        yield
        try:
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token
            
            payload = {
                "visit_id": self.selected_student["visit_id"],
                "complaint_id": self.selected_student["complaint_id"],
                "student_id": self.selected_student["student_id"],
                "diagnosis_description": self.current_diagnosis,
                "treatment_plan": self.current_treatment_plan
            }
            
            if self.edit_diagnosis:
                response = await Communicator.update_diagnose(self, self.edit_diagnoses_id, payload, auth)
            else:
                response = await Communicator.create_diagnoses(self, payload, auth)

            try:
                data = response.json()
                print(data)
                # self.selected_student = data
            except Exception as e:
                yield rx.toast.error(f"Error parsing response: {e}", position="top-right")
                return

            if response.status_code in (200, 201):
                self.close_diagnosis_dialog()
                self.add_diagnosis = response.json()
                yield rx.toast.success("Daignoses record saved successfully!", position="top-right")
            else:
                # Show error message from server
                error_msg = data.get("detail", "Failed to save faculty")
                yield rx.toast.error(error_msg, position="top-right")

        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"HTTP error occurred: {str(e)}", position="top-right")
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield rx.toast.error(
                "An unexpected error occurred. Please try again.", 
                position="top-right"
            )
        finally:
            self.is_diagnosis = False


    async def save_prescriptions(self):
        payload = []
        if not self.prescriptions:
            yield rx.toast.error("Please add at least one prescription", position="top-right")
            return
        for prescription in self.prescriptions:
            data = {
            "diagnosis_id": self.loaded_diagnosis["diagnosis_id"],
            "student_id": self.selected_student["student_id"],
            "drug_id": prescription["drug_id"],
            "dosage": prescription["dosage"],
            "instructions": prescription["instructions"]
            }
            payload.append(data)

        self.is_prescriptions = True
        yield
        try:
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token

            response = await Communicator.create_prescriptions(self, payload, auth)
            if response.status_code in (200, 201):
                self.prescriptions = []
                self.prescriptions = response.json()
                yield rx.toast.success("Prescription record saved successfully!", position="top-right")
                self.prescriptions.append(response.json()[0])
            else:
                # Show error message from server
                error_msg = data.get("detail", "Failed to save faculty")
                yield rx.toast.error(error_msg, position="top-right")
            print(response.json())
            
        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"HTTP error occurred: {str(e)}", position="top-right")
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield rx.toast.error(
                "An unexpected error occurred. Please try again.", 
                position="top-right"
            )
        finally:
            self.is_prescriptions = False   



    