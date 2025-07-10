import reflex as rx

from .pages import (index_page, admin_page, doctors_page, students_page, pharmacist_page, lab_attendance_page, super_signup)
from .states import auth_state, auth_student
# from .components import recovery, register, signin, signup

# Create the Reflex app
app = rx.App()
app.add_page(index_page.index, route="/")
app.add_page(super_signup.index, route="/super-signup")
app.add_page(auth_state.require_auth(admin_page.admin_page), route="/admin")
app.add_page(auth_state.require_auth(doctors_page.doctor_page), route="/doctor")
app.add_page(auth_student.require_auth(students_page.student_page), route="/student")
app.add_page(auth_state.require_auth(pharmacist_page.pharmercist_page), route="/pharmercist")
app.add_page(auth_state.require_auth(lab_attendance_page.lab_page), route="/lab-attendance")


