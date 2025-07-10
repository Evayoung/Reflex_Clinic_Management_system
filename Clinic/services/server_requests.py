import httpx
import asyncio
from urllib.parse import quote

BACKEND_URL = "http://localhost:8006"


class Communicator:
    def __init__(self):
        super().__init__(self)

        self.token: str = None

    async def set_token(self, token):
        self.token = token

    async def login(self, username, password):
        """Handle login and store user data."""
        payload = {
            "user_id": username,
            "password": password
            }
        # print(payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/auth/user/login", json=payload)

            return response
        
    async def student_login(self, username, password):
        """Handle login and store student data."""
        payload = {
            "matriculation_number": username,
            "password": password
            }
        # print(payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/auth/student/login", json=payload)
            
            return response

    

    async def create_session(self, session_name, token):
        """Handle login and store user data."""
        payload = {   
                "session_name": session_name,
                }

        # print(payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/admin/sessions", json=payload, headers={"Authorization": f"Bearer {token}"})

            return response
        
    async def create_level(self, level_name, token):
        """Handle login and store user data."""
        payload = {   
                "level_name": level_name,
                }

        # print(payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/admin/levels", json=payload, headers={"Authorization": f"Bearer {token}"})

            return response

            # /admin/students
        
    async def create_user(self, payload, token):
        """Handle login and store user data."""
        # print(payload)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/admin/users", json=payload, headers={"Authorization": f"Bearer {token}"})
            return response
        
        
    async def create_student(self, payload):
        """Handle student creation"""
        async with httpx.AsyncClient() as client:
            # print("the payload:", payload)
            response = await client.post(f"{BACKEND_URL}/admin/create-students", json=payload)

            return response
        
    async def update_student(self, student_id, payload):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BACKEND_URL}/admin/students/{student_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response

    async def create_department(self, payload, token):
        """Handle department creation data."""

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/admin/departments", json=payload, headers={"Authorization": f"Bearer {token}"})
            # print("the response:", response)
            return response
    
        
    async def get_details(self, token):
        """"""
        async with httpx.AsyncClient() as client:
            sessions, levels, users, faculties, departments, students, dashboard = await asyncio.gather(
                client.get(f"{BACKEND_URL}/admin/get-sessions", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/admin/get-levels", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/admin/users", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/admin/faculties"),
                client.get(f"{BACKEND_URL}/admin/departments"),
                client.get(f"{BACKEND_URL}/admin/students"),
                client.get(f"{BACKEND_URL}/admin/admin/get-admin-dashboard", headers={"Authorization": f"Bearer {token}"})
            )

            sessions.raise_for_status()
            levels.raise_for_status()
            users.raise_for_status()
            faculties.raise_for_status()
            departments.raise_for_status()
            students.raise_for_status()
            dashboard.raise_for_status()
            return sessions, levels, users, faculties, departments, students, dashboard
        

    


    async def update_level(self, token, level_id: int, level_name: str):

        payload = {   
                "level_name": level_name,
                }
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BACKEND_URL}/admin/update-level/{level_id}",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            return response

    async def update_session(self, token, session_id: int, session_name: str):

        payload = {   
                "session_name": session_name,
                }
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BACKEND_URL}/admin/update-session/{session_id}",
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            return response
        

    async def update_user(self, token, user_id: str, payload: dict):
        user_id_encoded = quote(user_id, safe='')
        url = f"{BACKEND_URL}/admin/users/{user_id_encoded}"
        print("Encoded URL:", url)
        async with httpx.AsyncClient() as client:
            response = await client.put(url,
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            return response
        
        
    async def create_faculty(self, payload: dict, token: str):
        """Create faculty and return full faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/admin/faculties",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response
        

    async def update_faculty(self, faculty_id: str, payload: dict, token: str):
        """Update faculty and return updated faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BACKEND_URL}/admin/update-faculty/{faculty_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response


    async def create_department(payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/admin/departments",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

    async def update_department(department_id: int, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{BACKEND_URL}/admin/update-department/{department_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
    

    # Doctors section
    async def get_doctor_details(self, token):
        """"""
        async with httpx.AsyncClient() as client:
            availability, schedules, dashboard, pending, drugs = await asyncio.gather(
                client.get(f"{BACKEND_URL}/doctor/availabilities", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/doctor/schedules", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/doctor/doctors/me/get-doctors-dashboard", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/doctor/doctor/visits", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/general/drugs"),
            )

            availability.raise_for_status()
            schedules.raise_for_status()
            
            return availability, schedules, dashboard, pending, drugs
        

    async def create_availability(payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/doctor/availabilities",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

    async def update_availability(availability_id: int, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{BACKEND_URL}/doctor/availability/{availability_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

    async def create_doctor_schedule(self, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/doctor/schedules",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
        
    
    async def update_doctor_schedule(self, schedule_id: int, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{BACKEND_URL}/doctor/schedules/{schedule_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

    async def update_doctor_schedule(self, schedule_id: int, token: str):
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{BACKEND_URL}/doctor/schedules/{schedule_id}/cancel",
                headers={"Authorization": f"Bearer {token}"}
            )
        
    async def create_diagnoses(self, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/doctor/diagnoses",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
        
    async def create_prescriptions(self, payload: list, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/doctor/create-multi-prescriptions",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
    
    async def update_diagnose(self, schedule_id: int, payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{BACKEND_URL}/doctor/schedules/{schedule_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
        
    
    async def get_student_visit(visit_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/doctor/doctor/visits/{visit_id}/details"
            )
            return response
            
    async def get_visit_prescription(token: str, visit_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/doctor/visits/{visit_id}/prescriptions",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response

    async def get_visit_diagnoses(token: str, visit_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/doctor/visits/{visit_id}/diagnoses",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response
    

    async def complete_visits(self, visit_id: int, token: str):
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{BACKEND_URL}/doctor/visits/{visit_id}/complete",
                headers={"Authorization": f"Bearer {token}"}
            )
        
    # student data requests section
    # =========================================================================================================
    async def get_student_details(self, token):
        """"""
        async with httpx.AsyncClient() as client:
            profile, complaints, slots, dashboard = await asyncio.gather(
                client.get(f"{BACKEND_URL}/students/full-profile", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/students/me/all-visits", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/students/schedules/available", headers={"Authorization": f"Bearer {token}"}),
                client.get(f"{BACKEND_URL}/students/students/me/dashboard", headers={"Authorization": f"Bearer {token}"}),
            )

            profile.raise_for_status()
            complaints.raise_for_status()
            return profile, complaints, slots, dashboard
        

    @staticmethod
    async def get_full_visits(token: str, visit_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/students/me/visits/{visit_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response

    @staticmethod
    async def submit_complaint(payload: dict, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/students/complaints",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            return response

    # =========================================================== pharmercy ====================================================
    async def create_drug(self, payload: dict, token: str):
        """Create faculty and return full faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/pharmacist/drugs",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response
        

    async def update_drug(self, drug_id: str, payload: dict, token: str):
        """Update faculty and return updated faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{BACKEND_URL}/pharmacist/drugs/{drug_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response


    async def get_drugs():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/general/drugs")

            return response
        

    async def delete_drug(drug_id: int, token: str):
        async with httpx.AsyncClient() as client:
            return await client.delete(
                f"{BACKEND_URL}/pharmacist/drugs/{drug_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
        
    async def get_student_data(token: str, matric):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/pharmacist/students/search?matriculation_number={matric}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response
        
    async def get_student_prescription(token: str, student_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/pharmacist/prescriptions?student_id={student_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response
        
    async def get_drug_dispenced(token: str, student_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/pharmacist/dispensed_drugs?student_id={student_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response
        
    
    async def get_drug_lists():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/general/drugs")
            return response
        
    async def create_dispensation_record(self, payload: dict, token: str):
        """Create faculty and return full faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/pharmacist/dispensations",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response
    
# ==============================================================================================================
    # Lab Attendance
    async def create_health_record(self, payload: dict, token: str):
        """Create faculty and return full faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/lab/create-records/",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response


    async def update_health_record(self, matric: str, payload: dict, token: str):
        """Update faculty and return updated faculty data."""
        async with httpx.AsyncClient() as client:
            response = await client.put(  # Changed from put to patch
                f"{BACKEND_URL}/lab/update-records",
                params={"matric_number": matric},
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response

    async def get_health_record(self, token: str, matric_number: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/lab/get-health-records",
                params={"matric_number": matric_number},
                headers={"Authorization": f"Bearer {token}"}
                )

            return response


    async def get_all_tested_student():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/lab/get-all-records/")

            return response