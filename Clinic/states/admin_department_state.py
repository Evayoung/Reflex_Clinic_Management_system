# faculty_state.py
import reflex as rx
import httpx
from ..services.server_requests import Communicator
from ..states import admin_state


class AdminDepartmentState(rx.State):
    """State for managing departments."""
    
    # Department data
    departments: list[dict] = []
    department_name: str = ""
    faculties: list[dict] = []  
    all_faculties: list[str] = []
    selected_faculty_id: int = 0
    selected_faculty_name: str = ""
    
    # Pagination and UI controls
    current_page: int = 1
    items_per_page: int = 5
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "5"
    show_dialog: bool = False
    is_editing: bool = False
    edit_department_id: int | None = None
    create_department: bool = False
    search_query: str = ""
    sort_field: str = ""
    
    def set_department_name(self, data: str):
        self.department_name = data

    def set_selected_faculty(self, faculty_name: str):
        """Set the selected faculty ID from dropdown"""
        self.selected_faculty_name = faculty_name
        self.selected_faculty_id = [s["faculty_id"] for s in self.faculties if s.get("faculty_name") == faculty_name][0]
        

    async def get_faculties(self, data: dict | None = None, data2: dict | None = None,):
        """Fetch and sort the faculties"""
        if data:
            self.faculties = data
            self.all_faculties = [faculty["faculty_name"] for faculty in data]

        if data2:
            self.departments = data2
            

    # async def get_department(self, data: dict | None = None):
    #     """Fetch all department from backend."""
    #     if data:
    #         self.departments = data
    #         print(self.departments)

    def sort_department_by(self, field: str):
        """Sort students by the specified field."""
        self.sort_field = field
        if self.departments:
            self.departments = sorted(self.departments, key=lambda x: x.get(field, "").lower())
            # self.update_pagination()
            # print(f"Sorted students by {field}: {len(self.students)} students")

    
    @rx.var
    def filtered_departments(self) -> list[dict]:
        """Filter faculties based on search query."""
        if not self.search_query:
            return self.departments
        return [department for department in self.departments 
                if self.search_query.lower() in department["department_name"].lower()]
    
    @rx.var
    def paginated_departments(self) -> list[dict]:
        """Paginate the filtered departments."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_departments[start:end]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages."""
        return max(1, (len(self.filtered_departments) + self.items_per_page - 1) // self.items_per_page)
    
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
        self.show_choice = value
    
    def open_dialog(self, department: dict | None = None):
        """Open dialog for creating/editing department"""
        if department:
            self.is_editing = True
            self.edit_department_id = department["department_id"]
            self.department_name = department["department_name"]
            self.selected_faculty_id = department["faculty_id"]
            self.selected_faculty_name = department["faculty_name"]
        else:
            self.is_editing = False
            self.edit_department_id = None
            self.department_name = ""
            self.selected_faculty_id = self.faculties[0]["faculty_id"] if self.faculties else 0
        self.show_dialog = True
    
    def close_dialog(self):
        """Close the dialog."""
        self.show_dialog = False

    async def submit_department(self):
        """Handle department creation/update"""
        if not self.department_name or not self.selected_faculty_id:
            yield rx.toast.error("Please fill all fields", position="top-right")
            return

        self.create_department = True
        yield

        try:
            admin = await self.get_state(admin_state.UserAuthState)
            # payload = {
            #     "department_name": self.department_name,
            #     "faculty_id": self.selected_faculty_id
            # }

            payload = {
                "faculty_id": int(self.selected_faculty_id),
                "department_name": self.department_name
                }

            if self.is_editing:
                response = await Communicator.update_department(
                    self.edit_department_id, payload, admin.token
                )
            else:
                response = await Communicator.create_department(payload, admin.token)

            data = response.json()
            
            if response.status_code in (200, 201):
                if self.is_editing:
                    self.departments = [
                        data if dept["department_id"] == self.edit_department_id else dept 
                        for dept in self.departments
                    ]
                else:
                    self.departments.append(data)
                
                yield rx.toast.success("Department saved!", position="top-right")
                self.close_dialog()
            else:
                yield rx.toast.error(data.get("detail", "Operation failed"), position="top-right")

        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")
        finally:
            self.create_department = False
    