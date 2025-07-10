import reflex as rx
import httpx
from ..services.server_requests import Communicator
from ..states import auth_state
from typing import List, Dict

class LabAttendanceState(rx.State):
    navigator: str = "Dashboard"
    token: str = ""
    show_visit: bool = False
    current_view: str = "Dashboard"
    search_query: str = ""
    
    # Health records state
    health_records: list[dict] = []
    show_dialog: bool = False
    is_editing: bool = False
    current_record: dict = {}
    is_saving: bool = False

    show_view_dialog: bool = False
    selected_record: dict = {}
    
    # Form fields
    matric_number: str = ""
    blood_group: str = ""
    genotype: str = ""
    height: str = ""
    weight: str = ""
    test_date: str = ""
    notes: str = ""
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 10
    total_pages: int = 1

    is_logout: bool = False
    
    def logout(self):
        self.is_logout = True

    def cancel_logout(self):
        self.is_logout = False

    def confirm_logout(self):
        self.cancel_logout()
        return rx.redirect("/")
    
    async def change_lab_view(self, view: str):
        self.current_view = view
        self.navigator = view
        
    def set_search_query(self, value: str):
        self.search_query = value

        # Add missing setters
    def set_matric_number(self, value: str):
        self.matric_number = value
        
    def set_blood_group(self, value: str):
        self.blood_group = value
        
    def set_genotype(self, value: str):
        self.genotype = value
        
    def set_height(self, value: str):
        self.height = value
        
    def set_weight(self, value: str):
        self.weight = value
        
    def set_test_date(self, value: str):
        self.test_date = value
        
    def set_notes(self, value: str):
        self.notes = value

    async def change_lab_view(self, view: str):
        self.current_view = view
        self.navigator = view
        
    def set_search_query(self, value: str):
        self.search_query = value

    async def load_health_records(self):
        try:
            response = await Communicator.get_all_tested_student()
            if response.status_code == 200:
                self.health_records = response.json() or []  # Ensure it's always a list
                self.total_pages = max(1, (len(self.health_records) + self.items_per_page - 1) // self.items_per_page)
            else:
                print(f"Error loading health records: {response.text}")
        except Exception as e:
            print(f"Error loading health records: {e}")
            self.health_records = []  # Fallback to empty list
    
    

    @rx.var
    def paginated_records(self) -> list[dict]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.health_records[start:end]
    
    def open_dialog(self, record: dict | None):
        self.is_editing = record is not None
        self.current_record = record or {}
        
        if self.is_editing:
            self.matric_number = record.get("matric_number", "")
            self.blood_group = record.get("blood_group", "")
            self.genotype = record.get("genotype", "")
            self.height = str(record.get("height", ""))
            self.weight = str(record.get("weight", ""))
            self.test_date = record.get("test_date", "")
            self.notes = record.get("notes", "")
        
        self.show_dialog = True
    
    def close_dialog(self):
        self.show_dialog = False
        self.reset_form()
    
    def reset_form(self):
        self.matric_number = ""
        self.blood_group = ""
        self.genotype = ""
        self.height = ""
        self.weight = ""
        self.test_date = ""
        self.notes = ""
    

    async def submit_record(self):
        """Submit health record data to backend and update state with response."""
        # Validate required fields
        if not self.matric_number or not self.test_date:
            yield rx.toast.error("Matric number and test date are required", position="top-right")
            return
        
        self.is_saving = True 
        yield
        
        try:
            # Get auth token
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token
            
            # Prepare payload
            data = {
                "matric_number": self.matric_number,
                "blood_group": self.blood_group or None,
                "genotype": self.genotype or None,
                "height": float(self.height) if self.height else None,
                "weight": float(self.weight) if self.weight else None,
                "test_date": self.test_date,
                "notes": self.notes or None
            }
            
            # Make API call
            if self.is_editing:
                response = await Communicator.update_health_record(self, self.matric_number, data, auth)
            else:
                response = await Communicator.create_health_record(self, data, auth)

            # Handle response
            try:
                response_data = response.json()
                print(response_data)
            except Exception as e:
                yield rx.toast.error(f"Error parsing response: {e}", position="top-right")
                return

            if response.status_code in (200, 201):
                # Update state with returned data
                if self.is_editing:
                    # Find and update existing record
                    for i, record in enumerate(self.health_records):
                        if record["matric_number"] == self.matric_number:
                            self.health_records[i] = response_data
                            break
                else:
                    # Append new record to the list
                    self.health_records.append(response_data)
                
                # Reset form and close dialog
                self.reset_form()
                self.close_dialog()
                
                yield rx.toast.success(
                    "Health record saved successfully!", 
                    position="top-right"
                )
            else:
                # Show error message from server
                error_msg = response_data.get("detail", "Failed to save health record")
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
            self.is_saving = False
    
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
    
    def change_items_per_page(self, value: str):
        self.items_per_page = int(value)
        self.current_page = 1
        self.total_pages = max(1, len(self.health_records) // self.items_per_page)

    @rx.var
    def filtered_records(self) -> List[Dict]:
        """Filter records based on search query"""
        if not self.search_query:
            return self.health_records
            
        return [
            record for record in self.health_records
            if (self.search_query.lower() in record.get("student_name", "").lower() or 
                self.search_query.lower() in record.get("matric_number", "").lower())
        ]
    
    @rx.var
    def paginated_records(self) -> List[Dict]:
        """Paginate filtered records"""
        filtered = self.filtered_records
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return filtered[start:end] if isinstance(filtered, list) else []
    
    
    @rx.var
    def total_filtered_pages(self) -> int:
        """Calculate total pages for filtered results"""
        return max(1, (len(self.filtered_records) + self.items_per_page - 1) // self.items_per_page)
    
    
    def view_record(self, record: Dict):
        """Set record to view and open dialog"""
        self.selected_record = record
        self.show_view_dialog = True
    
    @rx.event
    async def handle_key_down(self, event):
        if event["key"] == "Enter":
            await self.search_records()

    async def search_records(self):
        """Trigger search and reset pagination"""
        self.current_page = 1
        self.total_pages = self.total_filtered_pages

    async def on_mount(self):
        async for _ in self.load_health_records():
            pass