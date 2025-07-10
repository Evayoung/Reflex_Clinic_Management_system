import reflex as rx

# Assuming you have a state like this for holding student data
# from ..states import student_profile_state

# --- Main Page Container ---
def student_profile_page():
    return rx.flex(
        rx.vstack(
            student_profile_card(), # The main comprehensive student profile
            portable_student_card(), # The smaller, portable clinic card
            align="center",
            spacing="5",
            width="100%",
            max_width="1000px", # Max width for the content for better readability
            padding="2rem",
            padding_top="0",
        ),
        justify="center",
        width="100%",
        padding="2rem",
        padding_top="0"
    )

# --- Comprehensive Student Profile Card ---
def student_profile_card():
    # Use a reactive state to access student data
    # For example: student_profile_state.student_full_data
    # This state would need to fetch the student, their latest health record, and their latest clinic card.
    return rx.box(
        rx.vstack(
            # Header Section (Name, Matric No, Status, Profile Picture)
            rx.hstack(
                rx.avatar(
                    src=student_profile_state.student_full_data.get("profile_picture", "/placeholder_avatar.jpg"),
                    size="8", # Larger avatar for profile
                    border="4px solid #fff",
                    box_shadow="xl",
                    margin_right="1.5rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{student_profile_state.student_full_data.get('surname', '')} {student_profile_state.student_full_data.get('first_name', '')}",
                        size="7",
                        color="#2d3748", # Darker text for readability
                        font_weight="extrabold",
                    ),
                    rx.text(
                        f"Matric No: {student_profile_state.student_full_data.get('matriculation_number', 'N/A')}",
                        color="#4a5568",
                        font_size="1.2em",
                        font_weight="semibold",
                    ),
                    rx.badge(
                        student_profile_state.student_full_data.get("status", "active").capitalize(),
                        color_scheme=rx.cond(student_profile_state.student_full_data.get("status") == "active", "green", "red"),
                        variant="solid",
                        margin_top="0.5em",
                    ),
                    align_items="start",
                    spacing="1",
                ),
                align="center",
                width="100%",
                padding_x="2rem",
                padding_top="2rem",
                padding_bottom="1rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#e2e8f0"),

            # Personal Details Section
            rx.box(
                rx.heading("Personal Details", size="5", margin_bottom="1rem", color="#2d3748"),
                rx.grid(
                    info_item("Email", student_profile_state.student_full_data.get("email", "N/A")),
                    info_item("Phone", student_profile_state.student_full_data.get("phone", "N/A")),
                    info_item("Date of Birth", student_profile_state.student_full_data.get("date_of_birth", "N/A")),
                    info_item("Gender", student_profile_state.student_full_data.get("gender", "N/A").capitalize()),
                    info_item("Address", student_profile_state.student_full_data.get("address", "N/A")),
                    info_item("Emergency Contact", student_profile_state.student_full_data.get("emergency_contact", "N/A")),
                    columns="repeat(auto-fit, minmax(280px, 1fr))", # Responsive grid
                    spacing="1.5rem",
                    width="100%",
                ),
                padding_x="2rem",
                padding_y="1.5rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#e2e8f0"),

            # Academic Details Section
            rx.box(
                rx.heading("Academic Information", size="5", margin_bottom="1rem", color="#2d3748"),
                rx.grid(
                    info_item("Faculty", student_profile_state.student_full_data.get("faculty_name", "N/A")),
                    info_item("Department", student_profile_state.student_full_data.get("department_name", "N/A")),
                    info_item("Level", student_profile_state.student_full_data.get("level_name", "N/A")),
                    info_item("Academic Session", student_profile_state.student_full_data.get("session_name", "N/A")),
                    columns="repeat(auto-fit, minmax(280px, 1fr))",
                    spacing="1.5rem",
                    width="100%",
                ),
                padding_x="2rem",
                padding_y="1.5rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#e2e8f0"),

            # Health Information Section
            rx.box(
                rx.heading("Health Information", size="5", margin_bottom="1rem", color="#2d3748"),
                rx.grid(
                    info_item("Blood Group", student_profile_state.student_full_data.get("blood_group", "N/A")),
                    info_item("Genotype", student_profile_state.student_full_data.get("genotype", "N/A")),
                    info_item("Height", rx.cond(student_profile_state.student_full_data.get("height"), f"{student_profile_state.student_full_data.get('height')} cm", "N/A")),
                    info_item("Weight", rx.cond(student_profile_state.student_full_data.get("weight"), f"{student_profile_state.student_full_data.get('weight')} kg", "N/A")),
                    info_item("Latest Test Date", student_profile_state.student_full_data.get("test_date", "N/A")),
                    info_item("Allergies", student_profile_state.student_full_data.get("allergies", "None provided")), # Assuming allergies is directly available or aggregated
                    columns="repeat(auto-fit, minmax(280px, 1fr))",
                    spacing="1.5rem",
                    width="100%",
                ),
                rx.box(
                    rx.text("Notes:", font_weight="bold", color="#4a5568", margin_top="1rem"),
                    rx.text(student_profile_state.student_full_data.get("notes", "No additional health notes."), color="#4a5568"),
                ),
                padding_x="2rem",
                padding_y="1.5rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#e2e8f0"),

            # Clinic Card Preview (can link to the actual card if desired)
            rx.box(
                rx.heading("Associated Clinic Card", size="5", margin_bottom="1rem", color="#2d3748"),
                rx.flex(
                    # This is where you can embed the portable_student_card directly if it's small enough,
                    # or just show key clinic card details with an option to view/print full card.
                    rx.center(
                        portable_clinic_card_display(), # A compact view of the clinic card
                        width="100%"
                    ),
                    justify="center",
                    width="100%",
                ),
                padding_x="2rem",
                padding_y="1.5rem",
            ),

            background_color="#ffffff", # White background for content
            border_radius="25px",
            box_shadow="lg", # More pronounced shadow for depth
            width="100%",
            spacing="0", # Control spacing between sections manually
        ),
        width="100%",
        max_width="900px", # Adjust max width for overall card
        margin_bottom="3rem", # Space below the main profile
    )

def info_item(label: str, value: str):
    return rx.box(
        rx.text(label, color="#718096", font_weight="bold", font_size="0.85em", margin_bottom="0.25em"),
        rx.text(value, color="#2d3748", font_size="1em", font_weight="medium"),
    )

# --- Smaller, Portable Student Clinic Card Design ---
def portable_clinic_card_display():
    # This will be embedded in the larger profile, or used stand-alone.
    # It focuses on clinic-relevant data.
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.avatar(
                    src=student_profile_state.student_full_data.get("profile_picture", "/placeholder_avatar.jpg"),
                    size="5",
                    border="2px solid #fff",
                ),
                rx.vstack(
                    rx.text(
                        f"{student_profile_state.student_full_data.get('surname', '')} {student_profile_state.student_full_data.get('first_name', '')}",
                        color="#fff",
                        font_weight="bold",
                        font_size="1.1em",
                    ),
                    rx.text(
                        f"Matric No: {student_profile_state.student_full_data.get('matriculation_number', 'N/A')}",
                        color="#d1d5db",
                        font_size="0.85em",
                    ),
                    rx.text(
                        f"{student_profile_state.student_full_data.get('department_name', 'N/A')}",
                        color="#d1d5db",
                        font_size="0.8em",
                    ),
                    align_items="start",
                    spacing="0",
                ),
                rx.spacer(),
                rx.image(
                    src=student_profile_state.student_full_data.get("qr_code", "/qr_placeholder.png"),
                    width="70px",
                    height="70px",
                    background="white",
                    padding="0.2rem",
                    border_radius="md",
                ),
                width="100%",
                align="center",
                spacing="3",
                padding="1rem",
            ),
            rx.divider(margin_y="0.5rem", border_color="#eee", opacity=0.5),
            rx.hstack(
                rx.vstack(
                    rx.text("Clinic ID", color="#c7d2fe", font_size="0.8em"),
                    rx.text(student_profile_state.student_full_data.get("clinic_number", "N/A"), color="#fff", font_weight="bold", font_size="1em"),
                    align_items="start",
                    spacing="1",
                ),
                rx.spacer(),
                rx.badge(
                    student_profile_state.student_full_data.get("card_status", "active"),
                    color_scheme=rx.cond(student_profile_state.student_full_data.get("card_status") == "active", "green", "red"),
                    variant="solid",
                ),
                width="100%",
                padding_x="1rem",
                padding_bottom="1rem",
                align="center",
            ),
        ),
        background="linear-gradient(135deg, #6366f1 0%, #a5b4fc 100%)", # Attractive gradient
        border_radius="15px",
        box_shadow="lg",
        width="100%",
        max_width="400px", # Make it noticeably smaller
        margin_top="1rem",
        margin_bottom="1rem",
    )