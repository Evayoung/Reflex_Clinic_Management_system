import reflex as rx
from datetime import time
from ..services.server_requests import Communicator
from ..states import auth_state

class DoctorScheduleState(rx.State):
    """State for managing doctor schedules following same pattern as availability."""
    
    # Schedule data
    schedules: list[dict] = []
    availabilities: list[dict] = []
    all_availabilities: list[str] = []
    show_start: str = ""
    show_stop: str = ""
    day: str = ""
    doctor_id: str = ""
    selected_availability_id: str = ""
    schedule_date: str = ""
    start_time: str = "09:00"  # Default values like availability
    end_time: str = "17:00"
    token: str = ""
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 10
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "10"
    
    # Dialog control
    show_dialog: bool = False
    is_editing: bool = False
    edit_schedule_id: int | None = None
    creating_schedule: bool = False
    
    # Search
    search_query: str = ""

    # ========== Form Setters ==========
    def set_selected_availability_id(self, value: str):
        self.selected_availability_id = value
        self.show_start = [s['start_time'] for s in self.availabilities if s['availability_id'] == int(value)][0] if value else ""
        self.show_stop = [e['end_time'] for e in self.availabilities if e['availability_id'] == int(value)][0] if value else ""
        self.day = [d['day_of_week'] for d in self.availabilities if d['availability_id'] == int(value)][0] if value else ""


    def set_schedule_date(self, value: str):
        self.schedule_date = value

    def set_start_time(self, value: str):
        self.start_time = value

    def set_end_time(self, value: str):
        self.end_time = value

    def set_search_query(self, value: str):
        self.search_query = value
        self.current_page = 1  # Reset to first page when searching

    async def get_schedules(self, data: dict | None = None, data2: dict | None = None):
        """Fetch schedules from the server"""
        if data:
            self.schedules = data

        if data2:
            self.availabilities = data2
            self.all_availabilities = [str(a["availability_id"]) for a in data2]
            # print(data2)
            # print(self.all_availabilities)
            

    # ========== Dialog Methods ==========
    def open_dialog(self, schedule: dict | None = None):
        """Open dialog for creating/editing following same pattern"""
        if schedule:
            self.is_editing = True
            self.edit_schedule_id = schedule["schedule_id"]
            self.selected_availability_id = str(schedule["availability_id"])
            self.schedule_date = schedule["date"]
            self.start_time = schedule["start_time"]
            self.end_time = schedule["end_time"]
        else:
            self.is_editing = False
            self.edit_schedule_id = None
            self.selected_availability_id = ""
            self.schedule_date = ""
            self.start_time = "09:00"
            self.end_time = "17:00"
        self.show_dialog = True
    
    def close_dialog(self):
        """Close the dialog"""
        self.show_dialog = False

    # ========== CRUD Operations ==========
    async def submit_schedule(self):
        """Submit schedule following same pattern as availability"""
        if not all([self.selected_availability_id, self.schedule_date]):
            yield rx.toast.error("Please fill all required fields", position="top-right")
            return
            
        if self.start_time >= self.end_time:
            yield rx.toast.error("End time must be after start time", position="top-right")
            return
            
        self.creating_schedule = True
        yield
        
        try:
            auth = await self.get_state(auth_state.UserAuthState)
            token = auth.token
            
            
            if self.is_editing:
                payload = {
                    "doctor_id": self.doctor_id,
                    "availability_id": int(self.selected_availability_id),
                    "date": self.schedule_date,
                    "start_time": self.start_time,
                    "end_time": self.end_time
                }
                response = await Communicator.update_doctor_schedule(self, self.edit_schedule_id, payload, token)
            else:
                payload = {
                    "availability_id": int(self.selected_availability_id),
                    "date": self.schedule_date,
                    "start_time": self.start_time,
                    "end_time": self.end_time
                }
                response = await Communicator.create_doctor_schedule(self, payload, token)
            
            if response.status_code in (200, 201):
                # Refresh data after successful operation
                if self.is_editing:
                    for i, sched in enumerate(self.schedules):
                        if sched["schedule_id"] == self.edit_schedule_id:
                            self.schedules[i] = response.json()
                            break
                else:
                    # Append new schedule to the list
                    self.schedules.append(response.json())
                self.close_dialog()
                yield rx.toast.success("Schedule saved!", position="top-right")
            
            else:
                error = response.json().get("detail", "Operation failed")
                yield rx.toast.error(f"Error: {error}", position="top-right")
                
        except Exception as e:
            yield rx.toast.error(f"Network error: {str(e)}", position="top-right")
        finally:
            self.creating_schedule = False

    async def cancel_schedule(self, schedule_id: int):
        """Cancel a schedule"""
        try:
            auth = await self.get_state(auth_state.UserAuthState)
            token = auth.token
            response = await Communicator.update_doctor_schedule(self, int(schedule_id), token)
            if response.status_code == 200:
                for i, sched in enumerate(self.schedules):
                        if sched["schedule_id"] == self.edit_schedule_id:
                            self.schedules[i] = response.json()
                            break
                yield rx.toast.success("Schedule cancelled", position="top-right")
            else:
                error = response.json().get("detail", "Failed to cancel")
                yield rx.toast.error(f"Error: {error}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"Network error: {str(e)}", position="top-right")

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
    def filtered_schedules(self) -> list[dict]:
        """Filter schedules based on search query"""
        if not self.search_query:
            return self.schedules
        return [
            s for s in self.schedules 
            if self.search_query.lower() in s.get("date", "").lower()
        ]
    
    @rx.var
    def paginated_schedules(self) -> list[dict]:
        """Paginate filtered schedules"""
        start = (self.current_page - 1) * self.items_per_page
        return self.filtered_schedules[start:start+self.items_per_page]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages"""
        return max(1, (len(self.filtered_schedules) + self.items_per_page - 1) // self.items_per_page)

    async def on_mount(self):
        """Load data on mount"""
        async for _ in self.fetch_preliminaries():
            pass