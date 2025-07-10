import reflex as rx
from typing import List, Optional
from datetime import date
from ..services.server_requests import Communicator
from ..states import auth_state

class DispensationState(rx.State):
    search_query: str = ""
    student: dict = {}
    prescriptions: List[dict] = []
    dispensed_drugs: List[dict] = []
    selected_prescription_id: int = 0
    selected_drug_id: int = 0
    selected_prescription: dict = {}
    quantity: str = ""
    dispense_date: str = ''
    selected_dispensed_drug: dict = {}
    drugs: List[dict] = []
    error_message: str = ""
    auth_token: str = ""  # Set this after login
    current_user: dict = {}  # Store user info from token (e.g., {"user_id": "UIL/23/123", "role": "pharmacist"})
    is_loading: bool = False
    is_dispensation: bool = False
    show_dispense_modal: bool = False
    show_view_modal: bool = False

    @rx.var
    def student_full_name(self) -> str:
        return (
            f"{self.student.get('first_name', '')} {self.student.get('surname', '')}"
            if self.student
            else ""
        )

    @rx.var
    def matriculation_number(self) -> str:
        return self.student.get("matriculation_number", "") if self.student else ""

    @rx.var
    def department_name(self) -> str:
        return self.student.get("department", {}).get("department_name", "") if self.student else ""

    @rx.var
    def faculty_name(self) -> str:
        return self.student.get("faculty", {}).get("faculty_name", "") if self.student else ""

    @rx.var
    def level_name(self) -> str:
        return self.student.get("level", {}).get("level_name", "") if self.student else ""

    @rx.var
    def email(self) -> str:
        return self.student.get("email", "") if self.student else ""

    @rx.var
    def phone(self) -> str:
        return self.student.get("phone", "") if self.student else ""

    @rx.var
    def date_of_birth(self) -> str:
        return self.student.get("date_of_birth", "") if self.student else ""

    @rx.var
    def gender(self) -> str:
        return self.student.get("gender", "") if self.student else ""

    @rx.var
    def emergency_contact(self) -> str:
        return self.student.get("emergency_contact", "") if self.student else ""

    @rx.var
    def base_url(self) -> str:
        return "http://localhost:8000"  # Update with your actual API URL

    async def search_student(self):
        self.error_message = ""
        if not self.search_query:
            yield rx.toast.warning("Please enter student matriculation number", position="top-right")
            return
        
        self.is_loading = True
        yield
        try:
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token
            response = await Communicator.get_student_data(auth, self.search_query)
            if response.status_code == 200:
                self.student = response.json()
                
                try:
                    pres = await Communicator.get_student_prescription(auth, self.student["student_id"])
                    disp = await Communicator.get_drug_dispenced(auth, self.student["student_id"])
                    drug = await Communicator.get_drug_lists()
                    
                    if pres.status_code == 200:
                        
                        self.prescriptions = pres.json()
                    else:
                        self.prescriptions = []

                    if disp.status_code == 200:
                        self.dispensed_drugs = disp.json()
                    else:
                        self.dispensed_drugs = []

                    if drug.status_code == 200:
                        self.drugs = drug.json()
                    else:
                        self.drugs = []
                    
                except Exception as e:
                    print(e)
            else:
                self.student = None
                self.prescriptions = []
                self.dispensed_drugs = []
                self.error_message = response.json().get("detail", "Failed to find student")
                rx.toast.error(self.error_message)
        except Exception as e:
            print(e)
        finally:
            self.is_loading = False
            

    def open_dispense_modal(self, prescription_id: int):
        self.selected_prescription_id = prescription_id
        for prescription in self.prescriptions:
            if prescription["prescription_id"] == prescription_id:
                self.selected_drug_id = prescription["drug_id"]
                self.selected_prescription = prescription
                break
        self.show_dispense_modal = True

    def close_dispense_modal(self):
        self.selected_prescription_id = None
        self.selected_drug_id = None
        self.selected_prescription = None
        self.quantity = ""
        self.dispense_date = None
        self.show_dispense_modal = False

    async def dispense_drug(self):
        if not self.selected_drug_id or not self.quantity or not self.dispense_date:
            self.error_message = "Please fill all fields"
            yield rx.toast.error(self.error_message, position="top-right")
            return
        
        self.is_dispensation = True
        yield
        try:
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token
            payload = {
                "prescription_id": self.selected_prescription_id,
                "student_id": self.student["student_id"],
                "drug_id": self.selected_drug_id,
                "quantity": self.quantity,
                "dispense_date": self.dispense_date
            }
            response = await Communicator.create_dispensation_record(self, payload, auth)
            if response.status_code == 200:
                # print(response.json())
                self.dispensed_drugs.append(response.json())
                self.close_dispense_modal()
                yield rx.toast.success("Drug dispensed successfully", position="top-right")
                
            else:
                self.error_message = response.json().get("detail", "Failed to dispense drug")
                yield rx.toast.error(f"{response.json()["detail"]}", position="top-right")
        except Exception as e:
            print(e)
            yield rx.toast.error(f"{response.json()["detail"]}", position="top-right")
        finally:
            self.is_dispensation = False

    def open_view_modal(self, drug_given_id: int):
        for dispensed_drug in self.dispensed_drugs:
            if dispensed_drug["drug_given_id"] == drug_given_id:
                self.selected_dispensed_drug = dispensed_drug
                break
        self.show_view_modal = True

    def close_view_modal(self):
        self.selected_dispensed_drug = None
        self.show_view_modal = False

    def set_search_query(self, query: str):
        self.search_query = query

    def set_quantity(self, quantity: str):
        self.quantity = quantity

    def set_dispense_date(self, dispense_date: str):
        self.dispense_date = dispense_date