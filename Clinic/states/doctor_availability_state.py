# doctor_availability_state.py
import reflex as rx
from datetime import time
from enum import Enum
from ..services.server_requests import Communicator
from ..states import auth_state, doctor_schedule_state, doctor_visit_state


class DoctorAvailabilityState(rx.State):
    """State for managing doctor availability schedules."""
    
    # Availability data
    availabilities: list[dict] = []
    doctor_id: str = ""
    week_days: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week: str = "Monday"
    start_time: str = "09:00"
    end_time: str = "17:00"
    all_status: list[str] = ["active", "inactive"]
    status: str = "active"
    token: str = ""

    dashboard_data: dict = {}
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 10
    show_choices: list[str] = ["10", "20", "50"]
    show_choice: str = "10"
    
    # Dialog control
    show_dialog: bool = False
    is_editing: bool = False
    edit_availability_id: int | None = None
    creating_availability: bool = False

    def set_day_of_week(self, value: str):
        self.day_of_week = value

    def set_start_time(self, value: str):
        self.start_time = value

    def set_end_time(self, value: str):
        self.end_time = value

    def set_status(self, value: str):
        self.status = value
    
    # Search
    search_query: str = ""
    pending_visits: list[dict] = []
    pending_visits_lists: str = ""
    appointments: list[dict] = []
    appointment_lists: str = ""
    total_visits: int = 0


    
    async def fetch_preliminaries(self):
        yield
        
        try:
            auth = await self.get_state(auth_state.UserAuthState)
            schedule = await self.get_state(doctor_schedule_state.DoctorScheduleState)
            visits = await self.get_state(doctor_visit_state.DoctorVisitState)
            
            self.token = auth.token
            response, response2, response3, response4, response5 = await Communicator.get_doctor_details(self, self.token)
            
            self.availabilities = response.json()
            self.dashboard_data = response3.json()
            await schedule.get_schedules(response2.json(), response.json())
            await visits.get_pending_data(response4.json(), response5.json())
            
            self.pending_visits = self.dashboard_data["pending_visits"]
            self.pending_visits_lists = str(len(self.pending_visits))
            self.appointments = self.dashboard_data["upcoming_appointments"]
            self.appointment_lists = str(len(self.appointments))
            self.total_visits = self.dashboard_data["total_completed_visits"]

        except Exception as e:
            print(e)
            
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")

    
    @rx.var
    def filtered_availabilities(self) -> list[dict]:
        """Filter availabilities based on search query."""
        if not self.search_query:
            return self.availabilities
        return [avail for avail in self.availabilities 
                if self.search_query.lower() in avail["day_of_week"].lower()]
    
    @rx.var
    def paginated_availabilities(self) -> list[dict]:
        """Paginate the filtered availabilities."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_availabilities[start:end]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages."""
        return max(1, (len(self.filtered_availabilities) + self.items_per_page - 1) // self.items_per_page)
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
    
    def change_items_per_page(self, value: str):
        """Change items per page."""
        self.items_per_page = int(value)
        self.current_page = 1
    
    def open_dialog(self, availability: dict | None = None):
        """Open dialog for creating/editing availability."""
        if availability:
            self.is_editing = True
            self.edit_availability_id = availability["availability_id"]
            self.day_of_week = availability["day_of_week"]
            self.start_time = availability["start_time"]
            self.end_time = availability["end_time"]
            self.status = availability["status"]
        else:
            self.is_editing = False
            self.edit_availability_id = None
            self.day_of_week = "Monday"
            self.start_time = "09:00"
            self.end_time = "17:00"
            self.status = "active"
        self.show_dialog = True
    
    def close_dialog(self):
        """Close the dialog."""
        self.show_dialog = False
    
    async def submit_availability(self):
        """Improved submission with better error handling"""
        if not all([self.day_of_week, self.start_time, self.end_time]):
            yield rx.toast.error("Please fill all required fields", position="top-right")
            return
        
        self.creating_availability = True
        yield
        
        try:
            payload = {
                "doctor_id": self.doctor_id,
                "day_of_week": self.day_of_week,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "status": self.status
            }
            
            if self.is_editing:
                response = await Communicator.update_availability(
                    self.edit_availability_id, 
                    payload,
                    self.token
                )
            else:
                response = await Communicator.create_availability(
                    payload,
                    self.token
                )
            
            if response.status_code in (200, 201):
                # Refresh the list after successful operation
                if self.is_editing:
                    for i, avail in enumerate(self.availabilities):
                        if avail["availability_id"] == self.edit_availability_id:
                            self.availabilities[i] = response.json()
                            break
                else:
                    self.availabilities.append(response.json())

                self.close_dialog()
                yield rx.toast.success("Schedule saved!", position="top-right")
            else:
                error = response.json().get("detail", "Operation failed")
                yield rx.toast.error(f"Error: {error}", position="top-right")
                
        except Exception as e:
            yield rx.toast.error(
                f"Network error: {str(e)}", 
                position="top-right"
            )
        finally:
            self.creating_availability = False

    async def on_mount(self):
        async for _ in self.fetch_preliminaries():
            pass