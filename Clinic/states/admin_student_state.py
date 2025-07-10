import reflex as rx
from datetime import datetime
import httpx
import os
import base64
from ..services.server_requests import Communicator
from .auth_state import UserAuthState
BACKEND_URL = "http://127.0.0.1:8006"

class AdminStudentState(rx.State):
    """Handles Student logic from admin."""
    
    # State variables (keep your existing ones)
    create_student: bool = False
    is_student: bool = False
    matriculation_number: str = ""
    first_name: str = ""
    surname: str = ""
    email: str = ""
    session: str = ""
    phone: str = ""
    date_of_birth: str = datetime.now().strftime("%Y-%m-%d")
    gender: str = ""
    address: str = ""
    role: str = "student"
    password: str = ""
    faculty_id: str = ""
    department_id: str = ""
    level: str = ""
    emergency_contact: str = ""
    profile_picture: str = ""
    status: str = "active"

    raw_faculties: list[dict] = []  
    raw_departments: list[dict] = []
    raw_levels: list[dict] = [] 
    raw_sessions: list[dict] = []    
    
    genders: list[str] = ["Male", "Female"]
    faculties: list[str] = []  # Example data
    faculty: str = ""
    all_sessions: list[str] = []
    all_levels: list[str] = []
    
    departments: list[str] = []  # Example data
    department: str = ""
    
    students: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_students: list[dict] = []
    students_cache: dict[str, list[dict]] = {}
    sort_field: str = "matriculation_number"
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "5"
    search_query: str = ""
    student_response: str = ""

    selected_student: dict = {}
    show_student_dialog: bool = False

    is_editing: bool = False
    editing_student_id: str = ""

    def set_edit_student(self, student: dict):
        """Set the student for editing and open the dialog."""
        self.is_editing = True
        self.editing_student_id = student.get("student_id", "")
        self.matriculation_number = student.get("matriculation_number", "")
        self.first_name = student.get("first_name", "")
        self.surname = student.get("surname", "")
        self.email = student.get("email", "")
        self.session = student.get("session_name", "")
        self.phone = student.get("phone", "")
        self.date_of_birth = student.get("date_of_birth", datetime.now().strftime("%Y-%m-%d"))
        self.gender = student.get("gender", "").capitalize()
        self.address = student.get("address", "")
        self.faculty = student.get("faculty_name", "")
        self.department = student.get("department_name", "")
        self.level = student.get("level_name", "")
        self.emergency_contact = student.get("emergency_contact", "")
        self.profile_picture = student.get("profile_picture", "")
        self.status = student.get("status", "active")
        self.create_student = True  # Open the dialog


    def set_selected_student(self, student: dict):
        """Set the selected student and open the dialog."""
        self.selected_student = student
        self.show_student_dialog = True

    def set_show_student_dialog(self, value: bool):
        """Set the show student dialog state."""
        self.show_student_dialog = value
        if not value:
            self.selected_student = {}
    
    
    async def get_students(self, students: list[dict], faculties: list[dict] = None, levels: list[dict] = None, sessions: list[dict] = None):
        """Fetch students from the main admin state."""
        self.raw_faculties = faculties if faculties else []
        self.raw_levels = levels if levels else []
        self.raw_sessions = sessions if sessions else []
        self.students = [student for student in students] if students else []
        self.faculties = [faculty["faculty_name"] for faculty in faculties] if faculties else []
        self.all_sessions = [session["session_name"] for session in sessions] if sessions else []
        self.all_levels = [level["level_name"] for level in levels] if levels else []
        
        self.update_pagination()
    

    async def update_student(self):
        """Handle student update."""
        self.is_student = True
        
        # Validate required fields
        required_fields = {
            # "Matric Number": self.matriculation_number,
            "First Name": self.first_name,
            "Surname": self.surname,
            "Email": self.email,
            "Session": self.session,
            "Phone": self.phone,
            "Gender": self.gender,
            "Faculty": self.faculty,
            "Department": self.department,
            "Level": self.level,
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            self.is_student = False
            yield rx.window_alert(f"Missing required fields: {', '.join(missing_fields)}")
            return
        
        try:
            # Prepare student data
            student_data = {
                # "matriculation_number": self.matriculation_number.upper(),
                "first_name": self.first_name.capitalize(),
                "surname": self.surname.capitalize(),
                "email": self.email,
                "session": self.session,
                "phone": self.phone,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender.lower(),
                "address": self.address,
                "role": self.role,
                "faculty": self.faculty,
                "department": self.department,
                "level": self.level,
                "emergency_contact": self.emergency_contact,
                "profile_picture": self.profile_picture,
                "status": self.status,
            }
            
            # Make API call
            response = await Communicator.update_student(self, self.editing_student_id, student_data)
            
            # Handle response
            if response.status_code == 200:
                data = response.json()
                # Update the student in the students list
                for i, student in enumerate(self.students):
                    if student.get("student_id") == self.editing_student_id:
                        self.students[i] = data
                        break
                self.update_pagination()
                self.reset_student_form()
                self.is_editing = False
                self.editing_student_id = ""
                yield rx.window_alert("Student updated successfully!")
            else:
                error_msg = response.json().get("detail", "Update failed")
                yield rx.window_alert(f"Error: {error_msg}")
                
        except httpx.HTTPStatusError as e:
            error_msg = e.response.json().get("detail", str(e))
            yield rx.window_alert(f"HTTP Error: {error_msg}")
        except Exception as e:
            yield rx.window_alert(f"Unexpected error: {str(e)}")
        finally:
            self.is_student = False
    
    async def register_student(self):
        """Handle student registration."""
        
        # Validate required fields
        required_fields = {
            "Matric Number": self.matriculation_number,
            "First Name": self.first_name,
            "Surname": self.surname,
            "Email": self.email,
            "Session": self.session,
            "Phone": self.phone,
            "Gender": self.gender,
            "Faculty": self.faculty,
            "Department": self.department,
            "Level": self.level,
            "Password": self.password
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            self.is_student = False
            yield rx.window_alert(f"Missing required fields: {', '.join(missing_fields)}")
            return
        
        self.is_student = True
        yield
        try:
            
            # Prepare student data
            student_data = {
                "matriculation_number": self.matriculation_number.upper(),
                "first_name": self.first_name.capitalize(),
                "surname": self.surname.capitalize(),
                "email": self.email,
                "session_id": [s["session_id"] for s in self.raw_sessions if s["session_name"] == self.session][0],
                "phone": self.phone,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender.lower(),
                "address": self.address,
                "role": "student",
                "password": self.password.lower(),
                "faculty_id": [f["faculty_id"] for f in self.raw_faculties if f["faculty_name"] == self.faculty][0],
                "department_id": [d["department_id"] for d in self.raw_departments if d["department_name"] == self.department][0],
                "level_id": [l["level_id"] for l in self.raw_levels if l["level_name"] == self.level][0],
                "emergency_contact": self.emergency_contact,
                "profile_picture": self.profile_picture,
                "status": self.status
                }
            
            response = await Communicator.create_student(self, student_data)
            
            # Handle response
            if response.status_code == 201:
                data = response.json()
                print(data)
                self.students.append(data)  
                self.reset_student_form()
                yield rx.toast.success("Student registered successfully!", position="top-right")
                # yield self.get_students()  # Refresh the full list
            else:
                error_msg = response.json().get("detail", "Registration failed")
                yield rx.toast.warning(f"Error: {error_msg}", position="top-right")
                
        except httpx.HTTPStatusError as e:
            error_msg = e.response.json().get("detail", str(e))
            yield rx.toast.error(f"HTTP Error: {error_msg}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")
        finally:
            self.update_pagination()
            self.is_student = False
    
    def reset_student_form(self):
        """Reset all student form fields."""
        self.matriculation_number = ""
        self.first_name = ""
        self.surname = ""
        self.email = ""
        self.session = ""
        self.phone = ""
        self.date_of_birth = datetime.now().strftime("%Y-%m-%d")
        self.gender = ""
        self.address = ""
        self.password = ""
        self.faculty = ""
        self.department = ""
        self.level = ""
        self.emergency_contact = ""
        self.profile_picture = ""
        self.create_student = False


    def update_pagination(self):
        """Update paginated students based on current page and filters."""
        filtered_students = self.students
        if self.search_query:
            filtered_students = [
                s for s in self.students
                if (self.search_query.lower() in s["first_name"].lower() or
                    self.search_query.lower() in s["surname"].lower() or
                    self.search_query.lower() in s["matriculation_number"].lower())
            ]
        
        # Apply faculty/department filters
        if self.faculty:
            filtered_students = [s for s in filtered_students if s.get("faculty_name") == self.faculty]
        if self.department:
            filtered_students = [s for s in filtered_students if s.get("department_name") == self.department]
        
        # Sort students
        if self.sort_field:
            filtered_students = sorted(
                filtered_students,
                key=lambda x: x.get(self.sort_field, "").lower()
            )
        
        # Paginate results
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        self.paginated_students = filtered_students[start_idx:end_idx]
    
    def next_page(self):
        """Go to the next page of results."""
        total_pages = (len(self.students) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_pagination()
    
    def prev_page(self):
        """Go to the previous page of results."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()
    
    def change_items_per_page(self, value: str):
        """Change the number of items displayed per page."""
        self.items_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self.update_pagination()
    
    def search_students(self, query: str):
        """Search students by name or matric number."""
        self.search_query = query
        self.current_page = 1
        self.update_pagination()
    
    def change_matric(self, value: str):
        """Change the select value var."""
        self.matriculation_number = value

    def change_first_name(self, value: str):
        """Change the select value var."""
        self.first_name = value

    def change_surname(self, value: str):
        """Change the select value var."""
        self.surname = value

    def change_email(self, value: str):
        """Change the select value var."""
        self.email = value

    def change_session(self, value: str):
        """Change the select value var."""
        self.session = value

    def change_phone(self, value: str):
        """Change the select value var."""
        self.phone = value

    def change_date_of_birth(self, value: str):
        """Change the select value var."""
        self.date_of_birth = value

    def change_gender(self, value: str):
        """Change the select value var."""
        self.gender = value

    def change_address(self, value: str):
        """Change the select value var."""
        self.address = value

    def change_role(self, value: str):
        """Change the select value var."""
        self.role = value

    def change_password(self, value: str):
        """Change the select value var."""
        self.password = value

    def change_level(self, value: str):
        """Change the select value var."""
        self.level = value


    def change_department(self, value: str):
        """Change the select value var."""
        self.department = value

    async def change_faculty(self, value: str):
        """Change the select value var."""
        self.faculty = value
        yield
        async for _ in self.fetch_department(value):
            pass  # Iterate over the async generator to execute it

    def change_emergency_contact(self, value: str):
        """Change the select value var."""
        self.emergency_contact = value

    def change_status(self, value: str):
        """Change the select value var."""
        self.status = value

    def sort_students_by(self, field: str):
        """Sort students by the specified field."""
        self.sort_field = field
        if self.students:
            # Handle 'name' as a combination of first_name and surname
            sort_key = field
            if field == "name":
                sort_key = lambda x: f"{x.get('first_name', '').lower()} {x.get('surname', '').lower()}"
            else:
                sort_key = lambda x: x.get(field, "").lower()
            self.students = sorted(self.students, key=sort_key)
            self.update_pagination()
    

    def set_create_student(self, value: bool):
        """Set the create student dialog state."""
        self.create_student = value
        if not value:
            self.reset_student_form()
            self.is_editing = False
            self.editing_student_id = ""

    
    async def handle_upload(self, files: list[rx.UploadFile]): 
        """Handle the upload of file(s) while keeping filename for display and Base64 for backend."""
        if not files:
            yield rx.toast.warning("No file selected.", position="top-right")
            return

        file = files[0]  # Only handle the first file

        # Check file size (5MB limit)
        file_content = await file.read()
        file_size = len(file_content) / (1024 * 1024)  # Convert to MB
        if file_size > 5:
            yield rx.toast.warning("File size must be less than 5MB.", position="top-right")
            return

        # Save the file locally
        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)
        outfile = upload_dir / file.name
        with outfile.open("wb") as file_object:
            file_object.write(file_content)

        # Store Base64 for backend
        self.profile_picture = base64.b64encode(file_content).decode('utf-8')
        if self.profile_picture:
            yield rx.toast.success("Profile picture uploaded successfully!", position="top-right")
        

    async def fetch_department(self, department: str):
        """Fetch group details from /group-details/."""
        try:
            async with httpx.AsyncClient() as client:
                
                # Use params instead of json to send query parameters
                response = await client.get(
                    f"{BACKEND_URL}/students/read-department/", 
                    params={"faculty": department}  
                )
                response.raise_for_status() 
                
                if response.status_code == 200:
                    data = response.json()
                    self.raw_departments = data
                    if len(data) > 0:
                        self.departments = [department["department_name"] for department in data]
                    else:
                        self.departments = []
                        self.department = ""
                
        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"Failed to fetch group details: {e.response.text}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"An error occurred: {str(e)}", position="top-right")
        # finally:
        #     self.loading = False
        #     yield  # Ensure UI updates after completion


    async def save_student(self):
        """Handle login and store user data."""
        if self.session == "":
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return

        self.create_session = True
        yield

        try:
            admin = await self.get_state(UserAuthState)
            auth = admin.token
            response = await Communicator.create_student(self, self.session, auth)
            
            try:
                data = response.json()
            except Exception as e:
                yield rx.toast.error(f"Error: {e}", position="top-right")
                return

            if response.status_code in [200, 201]:
                print(data)
                if self.editing_session:
                    for i in range(len(self.sessions)):
                        if self.sessions[i]["session_id"] == self.selected_session["session_id"]:
                            self.sessions[i] = data
                            break
                else:
                    self.sessions.append(data)
                self.update_pagination()
            else:
                yield rx.toast.error(data.get("detail", "Failed to save level"), position="top-right")

                self.sessions.append(data)
                self.update_pagination()
        except Exception as e:
            print(e)
            yield rx.toast.error(f"Login failed: {str(e)}", position="top-right")
        
        finally:
            self.create_session = False