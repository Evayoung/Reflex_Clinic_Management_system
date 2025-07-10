# faculty_state.py
import reflex as rx
import httpx
from ..services.server_requests import Communicator
from ..states import admin_state
from enum import Enum


class AdminFacultyState(rx.State):
    """State for managing faculties."""
    
    
    # Faculty data
    faculties: list[dict] = []
    faculty_name: str = ""
    faculty_types: list[str] = ["Arts", "Engineering", "Medical", "Education", "Sciences"]
    faculty_type: str = "Arts"  # Default type
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 5
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "5"
    
    # Dialog control
    show_dialog: bool = False
    is_editing: bool = False
    edit_faculty_id: int = None
    create_faculty: bool = False
    
    # Search
    search_query: str = ""
    
    def set_faculty_name(self, data: str):
        self.faculty_name = data

    def set_faculty_type(self, data: str):
        self.faculty_type = data

    async def get_faculties(self, data: dict | None = None):
        """Fetch all faculties from backend."""
        if data:
            self.faculties = data
        # token = await self.get_token()
        # response = await admin_state.AdminState.get_state(token)
        # if response.status_code == 200:
        #     self.faculties = response.json()
    
    @rx.var
    def filtered_faculties(self) -> list[dict]:
        """Filter faculties based on search query."""
        if not self.search_query:
            return self.faculties
        return [faculty for faculty in self.faculties 
                if self.search_query.lower() in faculty["faculty_name"].lower()]
    
    @rx.var
    def paginated_faculties(self) -> list[dict]:
        """Paginate the filtered faculties."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_faculties[start:end]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages."""
        return max(1, (len(self.filtered_faculties) + self.items_per_page - 1) // self.items_per_page)
    
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
    
    def open_dialog(self, faculty: dict | None = None):
        """Open dialog for creating/editing faculty."""
        if faculty:
            self.is_editing = True
            self.edit_faculty_id = faculty["faculty_id"]
            self.faculty_name = faculty["faculty_name"]
            self.faculty_type = faculty["faculty_type"]
        else:
            self.is_editing = False
            self.edit_faculty_id = 0
            self.faculty_name = ""
            self.faculty_type = self.faculty_type
        self.show_dialog = True
    
    def close_dialog(self):
        """Close the dialog."""
        self.show_dialog = False
    
    async def submit_faculty(self):
        """Submit faculty data to backend and update state with response."""
        # Validate inputs
        if not self.faculty_name or not self.faculty_type:
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return
        
        self.create_faculty = True
        yield
        try:
            # Get auth token
            admin = await self.get_state(admin_state.UserAuthState)
            auth = admin.token
            
            # Prepare payload
            payload = {
                "faculty_name": self.faculty_name,
                "faculty_type": self.faculty_type
            }

            # Make API call
            if self.is_editing:
                response = await Communicator.update_faculty(self, self.edit_faculty_id, payload, auth)
            else:
                response = await Communicator.create_faculty(self, payload, auth)

            # Handle response
            try:
                data = response.json()
            except Exception as e:
                yield rx.toast.error(f"Error parsing response: {e}", position="top-right")
                return

            if response.status_code in (200, 201):
                # Update state with returned data
                if self.is_editing:
                    # Find and update the existing faculty
                    for i, faculty in enumerate(self.faculties):
                        if faculty["faculty_id"] == self.edit_faculty_id:
                            self.faculties[i] = data
                            break
                else:
                    # Append new faculty to the list
                    self.faculties.append(data)
                
                # Reset form and close dialog
                self.faculty_name = ""
                self.faculty_type = self.faculty_types[0]  # Reset to default type
                self.close_dialog()
                
                yield rx.toast.success(
                    "Faculty saved successfully!", 
                    position="top-right"
                )
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
            self.create_faculty = False
    