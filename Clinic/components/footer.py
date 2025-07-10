import reflex as rx

# Define the footer component
def footer():
    return rx.box(
        rx.center(
            rx.text("© 2025, Quoin-lab Technology", color="white", font_size="12px"),
            bg="rgba(0, 0, 0, 0)",  # Semi-transparent black background
            padding="10px",
            width="100%",
            position="fixed",
            bottom="0",
            z_index="1000",
        ),
         width="100%",
         position="fixed",
    )


def alt_footer():
    return rx.box(
        rx.center(
            rx.text("© 2025, Quoin-lab Technology", color="#330099", font_size="12px"),
            bg="rgba(0, 0, 0, 0)",  # Semi-transparent black background
            padding="10px",
            width="100%",
            position="fixed",
            bottom="0",
            z_index="1000",
        ),
         width="100%",
         position="fixed",
    )

