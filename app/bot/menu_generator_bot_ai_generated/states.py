from aiogram.fsm.state import StatesGroup, State

class OrganizationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_type = State()
    waiting_for_menu = State()
    waiting_for_description_images = State()
    waiting_for_images = State()
