# faculty_state.py
import reflex as rx
import httpx
from ..services.server_requests import Communicator
from ..states import auth_state
from enum import Enum


class PharmercyDrugState(rx.State):
    """State for managing faculties."""
    
    drugs: list[dict] = []
    drug_name: str = ""
    drug_descriptions: str = ""
    stock_level: str = ""
    selected_drug: dict = {}
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 5
    show_choices: list[str] = ["5", "10"]
    show_choice: str = "5"
    
    # Dialog control
    show_dialog: bool = False
    is_editing: bool = False
    edit_drug_id: int = None
    create_drug: bool = False
    is_delete: bool = False
    
    # Search
    search_query: str = ""
    
    def set_drug_name(self, data: str):
        self.drug_name = data

    def set_drug_description(self, data: str):
        self.drug_descriptions = data
        
    def set_stock_level(self, data: str):
        self.stock_level = data

    async def get_drugs(self):
        """Fetch all faculties from backend."""
        yield
        try:
            response = await Communicator.get_drugs()
            self.drugs = response.json() if response.status_code == 200 else []
            # print(self.drugs)
        except Exception as e:
            print(e)
            yield rx.toast.error(f"Could not load drugs: {e}", position="top-right")


    async def open_delete_drug_dialog(self, drug_id):
        self.selected_drug = [drug for drug in self.drugs if drug["drug_id"] == drug_id][0]
        self.is_delete = True

    async def close_delete_drugs_dialog(self):
        self.is_delete = False


    async def continue_delet_drug(self):
        admin = await self.get_state(auth_state.UserAuthState)
        auth = admin.token
        try:
            response = await Communicator.delete_drug(self.selected_drug["drug_id"], auth)
            self.is_delete = False
            if response.json()["detail"] == "Drug deleted successfully":
                for i in self.drugs:
                    if i["drug_id"] == self.selected_drug["drug_id"]:
                        self.drugs.remove(i)
                        break
                    self.selected_drug = {}
                
                yield rx.toast.success(f"Drug deleted successfully!", position="top-right") 
            else:
                yield rx.toast.error(f"Error: {response.json()["detail"]}", position="top-right")
        except Exception as e:
            self.is_delete = False
            yield rx.toast.error(f"Drug could not be deleted: {e}", position="top-right")

    
    @rx.var
    def filtered_drugs(self) -> list[dict]:
        """Filter faculties based on search query."""
        if not self.search_query:
            return self.drugs
        return [drug for drug in self.drugs 
                if self.search_query.lower() in drug["name"].lower()]
    
    @rx.var
    def paginated_drugs(self) -> list[dict]:
        """Paginate the filtered faculties."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_drugs[start:end]
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages."""
        return max(1, (len(self.filtered_drugs) + self.items_per_page - 1) // self.items_per_page)
    
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
    
    def open_dialog(self, drug: dict | None = None):
        """Open dialog for creating/editing faculty."""
        if drug:
            self.is_editing = True
            self.edit_drug_id = drug["drug_id"]
            self.drug_name = drug["name"]
            self.drug_descriptions = drug["description"]
            self.stock_level = drug["stock_level"]
        else:
            self.is_editing = False
            self.edit_drug_id = 0
            self.drug_name = ""
            self.drug_descriptions = ""
            self.stock_level = ""
        self.show_dialog = True
    
    def close_dialog(self):
        """Close the dialog."""
        self.show_dialog = False
    
    async def submit_drug(self):
        """Submit faculty data to backend and update state with response."""
        # Validate inputs
        if not self.drug_name or not self.drug_descriptions or not self.stock_level:
            yield rx.toast.error("Please fill in all fields", position="top-right")
            return
        
        self.create_drug = True
        yield
        try:
            # Get auth token
            admin = await self.get_state(auth_state.UserAuthState)
            auth = admin.token
            
            # Prepare payload
            payload = {
                "name": self.drug_name,
                "description": self.drug_descriptions,
                "stock_level": int(self.stock_level)
                }

            # Make API call
            if self.is_editing:
                response = await Communicator.update_drug(self, self.edit_drug_id, payload, auth)
            else:
                response = await Communicator.create_drug(self, payload, auth)

            # Handle response
            try:
                data = response.json()
            except Exception as e:
                yield rx.toast.error(f"Error parsing response: {e}", position="top-right")
                return

            if response.status_code in (200, 201):
                # Update state with returned data
                if self.is_editing:
                    for i, drug in enumerate(self.drugs):
                        if drug["drug_id"] == self.edit_drug_id:
                            self.drugs[i] = data
                            break
                else:
                    # Append new faculty to the list
                    self.drugs.append(data)
                
                # Reset form and close dialog
                self.drug_name = ""
                self.drug_descriptions = ""  
                self.stock_level = ""
                self.close_dialog()
                
                yield rx.toast.success(
                    "drug record saved successfully!", 
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
            self.create_drug = False

    async def on_mount(self):
        async for _ in self.get_drugs():
            pass
    