import reflex as rx
from datetime import datetime
from ..services.server_requests import Communicator


class CardState(rx.State):
    """State for managing clinic card data"""
    card_data: dict = {}
    student_data: dict = {}
    student_info: dict = {}
    complaints: list[dict] = []
    loading: bool = True
    

    async def set_student_info(self, data: dict):
        self.student_info = data
        