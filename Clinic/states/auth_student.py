import reflex as rx
import httpx
import base64
import os
import asyncio
from datetime import datetime
from ..services.server_requests import Communicator
from ..states import card_state, student_complaint_state

BACKEND_URL = "http://127.0.0.1:8006"

class UserAuthState(rx.State):
    """Handles authentication logic."""

    is_authenticated: bool = rx.SessionStorage("false") == "true"
    token: str = rx.SessionStorage("")
    student_data: dict = {}

    values: list[str] = ["Male", "Female"]
    academic_sessions: list[str] = []
    faculties: list[str] = []
    departments: list[str] = []
    levels: list[str] = []

    session_id: str = ""
    faculty_id: str = ""
    department_id: str = ""
    level_id: str = ""

    raw_faculties: list[dict] = []
    raw_sessions: list[dict] = []
    raw_levels: list[dict] = []
    raw_departments: list[dict] = []
    
    surname: str = ""
    firstname: str = ""
    matric: str = ""
    email: str = ""
    phone: str = ""
    dob: str = ""
    value: str = "Male"
    academic_session: str = "2024 / 2025"
    address: str = ""
    faculty: str = "Arts"
    department: str = ""
    level: str = "100 Level"
    guidance: str = ""
    passport: str = ""
    submit: bool = False

    current_date: str = ""
    current_main: str = "Home"
    current_submain: str = "Default"


    # for user login data
    matric_number: str = ""
    password: str = ""
    loading: bool = False

    


    def change_main_view(self, view: str):
        """Change the main view of the landig page"""
        self.current_main = view

    def change_submain_view(self, view):
        """Toggle view for admin login and student login"""
        self.current_submain = view

    def change_matric_number(self, value: str):
        self.matric_number = value.upper()

    def change_password(self, value: str):
        """Change the select value var."""
        self.password = value


    def change_surname(self, value: str):
        self.surname = value.capitalize()

    def change_firstname(self, value: str):
        """Change the select value var."""
        self.firstname = value.capitalize()

    def change_matric(self, value: str):
        """Change the select value var."""
        self.matric = value.upper()
        
    def change_email(self, value: str):
        """Change the select value var."""
        self.email = value

    def change_phone(self, value: str):
        """Change the select value var."""
        self.phone = value

    def change_dob(self, value: str):
        """Change the select value var."""
        self.dob = value

    def change_value(self, value: str):
        """Change the select value var."""
        self.value = value

    def change_session(self, value: str):
        """Change the select value var."""
        self.academic_session = value

    def change_address(self, value: str):
        """Change the select value var."""
        self.address = value


    async def change_faculty(self, value: str):
        """Change the select value var."""
        self.faculty = value
        yield
        async for _ in self.fetch_department(value):
            pass  # Iterate over the async generator to execute it

    def change_department(self, value: str):
        """Change the select value var."""
        self.department = value
        
        # print([data["department_id"] for data in self.raw_departments if data["department_name"] == value][0])

    def change_guidance(self, value: str):
        """Change the select value var."""
        self.guidance = value

    def change_level(self, value: str):
        """Change the select value var."""
        self.level = value
        # self.level_id = [data["faculty_id"] for data in self.raw_faculties if data["faculty_name"] == self.faculty][0]
        # 
        

    def change_passport(self, view: str):
        self.passport = view

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

        # Save the file locally (keep original behavior)
        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)
        outfile = upload_dir / file.name  # Use .name instead of .filename
        with outfile.open("wb") as file_object:
            file_object.write(file_content)

        # Create a separate Base64 variable for backend transmission
        self.passport = base64.b64encode(file_content).decode('utf-8')
        if self.passport:
            yield rx.toast.success("Profile pictures uploaded sucessfully!", position="top-right")
        

    async def login(self):
        """Handle login and store user data."""
        if self.matric_number == "" or self.password == "":
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return
        
        self.loading = True

        yield
        try:
            card = await self.get_state(card_state.CardState)
            complaints = await self.get_state(student_complaint_state.StudentComplaintState)
            
            response = await Communicator.student_login(self, self.matric_number, self.password.lower())
            data = response.json()
            if response.status_code == 200 and data.get("access_token"):
                # await Communicator.set_token(self, data["access_token"])  # Store token in Communicator for future requests
                self.is_authenticated = True
                self.token = data["access_token"]
                self.student_data = data
                await card.set_student_info(data)
                await complaints.on_mount(data)
                now = datetime.now()
                self.current_date = now.strftime("%d %B, %Y")
                yield rx.redirect("/student")
            else:
                raise Exception("Invalid credentials")
        except Exception as e:
            print(e)
            yield rx.toast.error(f"Login failed: {str(e)}", position="top-right")
        
        finally:
            self.loading = False 
        
        
    
    async def logout(self):
        """Clear auth state and redirect."""
        self.token = ""
        self.student_data = {}
        return rx.redirect("/")
    
    async def fetch_preliminaries(self):
        """Fetch group details and other dashboard stats concurrently."""
        
        self.loading = True
        yield  

        try:
            async with httpx.AsyncClient() as client:
                
                all_faculties, all_levels, sessions = await asyncio.gather(
                    client.get(f"{BACKEND_URL}/students/faculties"),
                    client.get(f"{BACKEND_URL}/students/get-levels"),
                    client.get(f"{BACKEND_URL}/students/get-sessions"),
                )

                all_faculties.raise_for_status()
                all_levels.raise_for_status()
                sessions.raise_for_status()

                self.raw_faculties = all_faculties.json()
                self.raw_levels = all_levels.json()
                self.raw_sessions = sessions.json()

                self.faculties = [faculty["faculty_name"] for faculty in all_faculties.json()]
                self.levels = [level["level_name"] for level in all_levels.json()]
                self.academic_sessions = [session["session_name"] for session in sessions.json()]

        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"Failed to fetch preliminaries: {e.response.text}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"An error occurred: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  

    async def call_fetch_preliminary(self):
        """Fetch and display group details."""
        self.loading = True
        yield
        async for _ in self.fetch_preliminaries():
            pass  # Iterate over the async generator to execute it
        # self.show_details = True  # Open the dialog

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
        finally:
            self.loading = False
            yield  # Ensure UI updates after completion

    
    async def create_account(self):
        """Handle student enrollment with """
        # Validate required fields
        if not all([self.matric, self.firstname, self.surname, self.email, self.academic_session, self.phone, self.dob,
                self.value, self.address, self.faculty, self.department, self.level, self.guidance, self.passport]):
            yield rx.toast.error("Please fill all required fields", position="top-right")
            return

        self.submit = True
        yield

        try:
            # Helper function to safely get ID
            def get_id(data_list, name_field, name_value, id_field):
                matches = [data[id_field] for data in data_list 
                        if str(data[name_field]).lower() == str(name_value).lower()]
                if not matches:
                    raise ValueError(f"No matching {name_field} found for '{name_value}'")
                return matches[0]

            payload = {
                "matriculation_number": self.matric.upper(),
                "first_name": self.firstname.capitalize(),
                "surname": self.surname.capitalize(),
                "email": self.email.capitalize(),
                "session_id": get_id(self.raw_sessions, "session_name", self.academic_session, "session_id"),
                "phone": self.phone,
                "date_of_birth": self.dob,
                "gender": self.value.lower(),
                "address": self.address,
                "role": "student",
                "password": self.surname.lower(),
                "faculty_id": get_id(self.raw_faculties, "faculty_name", self.faculty, "faculty_id"),
                "department_id": get_id(self.raw_departments, "department_name", self.department, "department_id"),
                "level_id": get_id(self.raw_levels, "level_name", self.level, "level_id"),
                "emergency_contact": self.guidance,
                "profile_picture": self.passport,
                "status": "active"
            }

            print(payload)

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/students/create-students",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                print(response)
                # Handle response
                if response.status_code == 201:
                    self.reset_field()
                    yield rx.toast.success(f"Account created successfully!", position="top-right")

        except ValueError as e:
            yield rx.toast.error(f"Configuration error: {str(e)}", position="top-right")
            return

        except httpx.HTTPStatusError as e:
            print(e)
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            yield rx.toast.error(f"HTTP error: {error_detail}", position="top-right")
            return
            
        except Exception as e:
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")
            print(e)
            return
        finally:
            self.submit = False



    def reset_field(self):
        self.matric = ""
        self.firstname = ""
        self.surname = ""
        self.email = ""
        self.academic_session = ""
        self.phone = ""
        self.dob = ""
        self.value = ""
        self.address = ""
        self.suname = ""
        self.faculty = ""
        self.department = ""
        self.level = ""
        self.guidance = ""
        self.passport = ""


    

@staticmethod
def require_auth(page_func):
    """Protect pages from unauthenticated access."""
    def wrapper(*args, **kwargs):
        return rx.cond(
            UserAuthState.is_authenticated,
            page_func(*args, **kwargs),
            rx.fragment(rx.script("window.location.href = '/'"))
        )
    wrapper.__name__ = page_func.__name__  # Preserve the original function name
    return wrapper

