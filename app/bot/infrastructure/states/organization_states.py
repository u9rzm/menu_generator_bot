from aiogram.fsm.state import State, StatesGroup

class OrganizationStates(StatesGroup):
    """States for organization creation process"""
    
    # Organization creation states
    waiting_for_name = State()
    waiting_for_description = State()
    
    # Menu upload states
    waiting_for_menu_file = State()
    waiting_for_menu_sheets = State()
    
    # Image upload states
    waiting_for_logo = State()
    waiting_for_background = State()
    waiting_for_photo = State()
    
    # Theme selection states
    waiting_for_theme = State()
    
    # QR code generation states
    waiting_for_qr_type = State()
    waiting_for_qr_content = State()
    
    # Web page generation states
    waiting_for_web_confirmation = State() 