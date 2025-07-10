import reflex as rx
from datetime import datetime
from ..services.server_requests import Communicator
from ..states.auth_state import UserAuthState
from ..states import admin_faculty_state, admin_department_state, admin_student_state

class AdminState(rx.State):
    """Handles authentication logic."""
    
    # state management data
    current_view: str = "Dashboard"
    navigator: str = "Dashboard"
    token: str = ""

    session: str = ""
    level: str = ""

    dashboard_data: dict = {}

    # data for user creation
    surname: str = ""
    username: str = ""
    password: str = ""
    role: str = ""
    email: str = ""
    phone: str = ""
    status: str = "active"
    status_type: list[str] = ["active", "inactive"]
    roles: list[str] = ["admin", "doctor", "pharmacist", "lab_attendant"]

    is_session: bool = False
    is_level: bool = False
    is_user: bool = False
    editing_level:bool = False
    editing_session:bool = False
    editing_user:bool = False
    creating_user: bool = False
    edit_user: bool = False

    create_session: bool = False
    create_level: bool = False
    create_user: bool = False
    view_user: bool = False

    sessions: list[dict] = []
    levels: list[dict] = []
    current_session_page: int = 1
    current_level_page: int = 1
    items_per_page: int = 6
    paginated_session: list[dict] = []
    paginated_level: list[dict] = []
    paginated_user: list[dict] = []

    users: list[dict] = []

    selected_level: dict = {}
    selected_session: dict = {}
    selected_user: dict = {}
    
    session_response: str = ""
    level_response: str = ""
    user_response: str = ""

    students: list[dict] = []
    selected_student: dict = {}
    is_edit_student: bool = False

    is_logout: bool = False
    
    def logout(self):
        self.is_logout = True

    def cancel_logout(self):
        self.is_logout = False

    def confirm_logout(self):
        self.cancel_logout()
        return rx.redirect("/")

    def change_surname(self, data: str):
        self.surname = data

    def change_username(self, data: str):
        self.username = data

    def change_password(self, data: str):
        self.password = data

    def change_role(self, data: str):
        self.role = data

    def change_email(self, data: str):
        self.email = data

    def change_phone(self, data: str):
        self.phone = data

    def change_status(self, data: str):
        self.status = data


    def change_admin_view(self, view: str):
        self.current_view = view
        self.navigator = view


    def save_level(self):
        self.is_level = False

    def edit_session(self, session: str):
        self.is_session = True
        print(session)

    def edit_level(self, level_name: str):
        self.is_level = True
        self.editing_level = True
        level = next((level for level in self.levels if str(level["level_name"]) == str(level_name)), None)
        if level:
            self.selected_level = level
            self.is_level = True
            self.level = level["level_name"]
            yield  # Ensure UI updates
        else:
            yield rx.toast.error(f"The seleceted data {level_name} does not exist", position="top-right")
            print(f"No user found for user_id: {level_name}")

    def edit_session(self, session_name: str):
        self.is_session = True
        self.editing_session = True
        session = next((session for session in self.sessions if str(session["session_name"]) == str(session_name)), None)
        if session:
            self.selected_session = session
            self.is_session = True
            self.session = session["session_name"]
            yield  # Ensure UI updates
        else:
            yield rx.toast.error(f"The seleceted data {session_name} does not exist", position="top-right")
            print(f"No user found for user_id: {session_name}")

    def clear_user(self):
        self.surname = ""
        self.username = ""
        self.password = ""
        self.role = ""
        self.email = ""
        self.phone = ""
        self.status = "active"

    def edit_users(self, user_id: str):
        self.is_user = True
        self.clear_user()
        self.editing_user = True
        user = next((user for user in self.users if str(user["user_id"]) == str(user_id)), None)
        if user:
            self.selected_user = user
            self.is_user = True
            self.username = user["username"].split(' ')[1]
            self.surname = user["username"].split(' ')[0]
            self.password = ""
            self.role = user["role"]
            self.email = user["email"]
            self.phone = user["phone"]
            self.status = user["status"]
            yield  # Ensure UI updates
        else:
            yield rx.toast.error(f"The seleceted data {user_id} does not exist", position="top-right")
            print(f"No user found for user_id: {user_id}")

    def open_dialog(self, data: str):
        if data == "session":
            self.is_session = True
        elif data == "level":
            self.is_level = True

    def open_user_dialog(self, data: str):
        self.is_user = True
        if data == "create_new":
            self.creating_user = True
        else:
            self.edit_user = True

    def view_user_dialog(self, user_id: str):
        self.view_user = True
        user = next((user for user in self.users if str(user["user_id"]) == str(user_id)), None)
        if user:
            self.selected_user = user
            self.view_user = True
            yield  
        else:
            yield rx.toast.error(f"No user found for user_id: {user_id}", position="top-right")
            print(f"No user found for user_id: {user_id}")

    def close_dialog(self, data: str):
        if data == "session":
            self.is_session = False
            self.editing_session = False
            self.session = ""
        elif data == "level":
            self.is_level = False
            self.editing_level = False
            self.level = ""
        elif data == "user":
            self.view_user = False
            

    def close_user_dialog(self):
        self.is_user = False
        self.editing_user = False
        self.username = ""
        self.password = ""
        self.role = ""
        self.email = ""
        self.phone = ""
        self.status = "active"
        self.creating_user = False
        self.edit_user = False

    def set_session(self, session: str):
        self.session = session

    def set_level(self, level: str):
        self.level = level

    async def save_session(self):
        """Handle login and store user data."""
        if self.session == "":
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return

        self.create_session = True
        yield

        try:
            admin = await self.get_state(UserAuthState)
            auth = admin.token

            if self.editing_session:
                response = await Communicator.update_session(self, auth, self.selected_session["session_id"], self.session)
                print(self.selected_session["session_id"], "\n", self.session)
            else:
                response = await Communicator.create_session(self, self.session, auth)
            
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

    
    async def save_levels(self):
        """Handle saving new or edited level."""
        if self.level == "":
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return

        self.create_level = True
        yield

        try:
            admin = await self.get_state(UserAuthState)
            auth = admin.token

            if self.editing_level:
                response = await Communicator.update_level(self, auth, self.selected_level["level_id"], self.level)
                print(self.selected_level["level_id"], "\n", self.level)
            else:
                response = await Communicator.create_level(self, self.level, auth)

            try:
                data = response.json()
            except Exception:
                yield rx.toast.error("Invalid server response", position="top-right")
                return

            if response.status_code in [200, 201]:
                print(data)
                if self.editing_level:
                    for i in range(len(self.levels)):
                        if self.levels[i]["level_id"] == self.selected_level["level_id"]:
                            self.levels[i] = data
                            break
                else:
                    self.levels.append(data)
                self.update_level_pagination()
            else:
                yield rx.toast.error(data.get("detail", "Failed to save level"), position="top-right")

        except Exception as e:
            print(e)
            yield rx.toast.error(f"Operation failed: {str(e)}", position="top-right")

        finally:
            self.create_level = False


    async def save_user(self):
        """Handle saving new or edited level."""
        if not self.editing_user and self.surname == "":
            yield rx.toast.error("Please enter Surname", position="top-right")
            return

        if not self.editing_user and self.username == "":
            yield rx.toast.error("Please enter User name", position="top-right")
            return
        
        if not self.editing_user and self.role == "":
            yield rx.toast.error("Please select user Type", position="top-right")
            return
        
        if not self.editing_user and self.email == "":
            yield rx.toast.error("Please user E-mail", position="top-right")
            return
        
        if not self.editing_user and self.phone == "":
            yield rx.toast.error("Please enter Phone number", position="top-right")
            return

        self.create_user = True
        yield

        try:
            payload = {
                "username": f"{self.surname.capitalize()} {self.username.capitalize()}",
                "password": self.surname.lower(),
                "role": self.role,
                "email": self.email,
                "phone": self.phone,
                "status": self.status
                }
            
            if self.editing_user:
                
                response = await Communicator.update_user(self, self.token, self.selected_user["user_id"], payload)
            else:
                response = await Communicator.create_user(self, payload, self.token)

            try:
                data = response.json()
            except Exception as e:
                self.user_response = f"Error: {e}"
                yield rx.toast.error("Invalid server response", position="top-right")
                return

            if response.status_code in [200, 201]:
                # print(data)
                if self.editing_user:
                    for i in range(len(self.users)):
                        if self.users[i]["user_id"] == self.selected_user["user_id"]:
                            self.users[i] = data
                            break
                else:
                    self.users.append(data)
                self.update_user_pagination()
            else:
                yield rx.toast.error(data.get("detail", "Failed to save user"), position="top-right")

        except Exception as e:
            print(e)
            yield rx.toast.error(f"Operation failed: {str(e)}", position="top-right")

        finally:
            self.create_user = False
    
    
    async def fetch_preliminaries(self):
        yield
        
        try:
            auth_state = await self.get_state(UserAuthState)
            faculty_state = await self.get_state(admin_faculty_state.AdminFacultyState)
            department_state = await self.get_state(admin_department_state.AdminDepartmentState)
            students = await self.get_state(admin_student_state.AdminStudentState)
            self.token = auth_state.token
            response, response2, response3, response4, response5, response6, dashboard = await Communicator.get_details(self, self.token)
            
            self.sessions = response.json()
            self.levels = response2.json()
            self.users = response3.json()
            self.dashboard_data = dashboard.json()
            await faculty_state.get_faculties(response4.json())
            await department_state.get_faculties(response4.json(), response5.json())
            await students.get_students(response6.json(), response5.json(), response2.json(), response.json())
            # await department_state.get_department(response5.json())

            # print(self.users)
            self.update_level_pagination()
            self.update_user_pagination()
            self.update_pagination()
        except Exception as e:
            print(e)
            self.sessions = [{"error": f"Failed to fetch: {str(e)}"}]
            self.update_pagination()
            self.update_level_pagination()
            self.update_user_pagination()
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")


    async def reset_fields(self):
        self.admin_name = ""
        self.admin_email = ""
        self.password = ""


    @rx.var(cache=True)
    def session_length(self) -> int:
        return len(self.sessions)

    def next_page(self):
        if (self.current_session_page * self.items_per_page) < self.session_length:
            self.current_session_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_session_page > 1:
            self.current_session_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_session_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_session = self.sessions[start:end]

    def update_level_pagination(self):
        start = (self.current_level_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_level = self.levels[start:end]

    def update_user_pagination(self):
        self.paginated_user = self.levels

    @rx.var
    def selected_user_name(self) -> str:
        return self.selected_user.get('username') or 'N/A'

    @rx.var
    def selected_user_id(self) -> str:
        return self.selected_user.get('user_id') or 'N/A'

    @rx.var
    def selected_user_phone(self) -> str:
        return self.selected_user.get('phone') or 'N/A'

    @rx.var
    def selected_user_email(self) -> str:
        return self.selected_user.get('email') or 'N/A'

    @rx.var
    def selected_user_role(self) -> str:
        return self.selected_user.get('role') or 'N/A'
    
    @rx.var
    def selected_user_status(self) -> str:
        return self.selected_user.get('status') or 'N/A'


        
    
    async def on_mount(self):
        async for _ in self.fetch_preliminaries():
            pass

        