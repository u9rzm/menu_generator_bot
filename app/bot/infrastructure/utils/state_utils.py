from typing import Optional, Dict, Any, Type
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.bot.infrastructure.utils.logging_utils import log_state_change
from app.bot.infrastructure.exceptions.handler_exceptions import StateError

class BaseState(StatesGroup):
    """Base state class"""
    pass

def get_state_name(state: State) -> str:
    """Get state name"""
    return state.state if state else "None"

def get_state_data(state: FSMContext) -> Dict[str, Any]:
    """Get state data"""
    return state.get_data() if state else {}

def set_state_data(state: FSMContext, data: Dict[str, Any]) -> None:
    """Set state data"""
    if state:
        state.set_data(data)

def update_state_data(state: FSMContext, data: Dict[str, Any]) -> None:
    """Update state data"""
    if state:
        current_data = state.get_data()
        current_data.update(data)
        state.set_data(current_data)

def clear_state_data(state: FSMContext) -> None:
    """Clear state data"""
    if state:
        state.set_data({})

def get_state_value(state: FSMContext, key: str) -> Optional[Any]:
    """Get state value"""
    if state:
        return state.get_data().get(key)
    return None

def set_state_value(state: FSMContext, key: str, value: Any) -> None:
    """Set state value"""
    if state:
        data = state.get_data()
        data[key] = value
        state.set_data(data)

def remove_state_value(state: FSMContext, key: str) -> None:
    """Remove state value"""
    if state:
        data = state.get_data()
        data.pop(key, None)
        state.set_data(data)

def has_state_value(state: FSMContext, key: str) -> bool:
    """Check if state has value"""
    if state:
        return key in state.get_data()
    return False

def get_state_keys(state: FSMContext) -> list:
    """Get state keys"""
    if state:
        return list(state.get_data().keys())
    return []

def get_state_values(state: FSMContext) -> list:
    """Get state values"""
    if state:
        return list(state.get_data().values())
    return []

def get_state_items(state: FSMContext) -> list:
    """Get state items"""
    if state:
        return list(state.get_data().items())
    return []

def get_state_length(state: FSMContext) -> int:
    """Get state length"""
    if state:
        return len(state.get_data())
    return 0

def is_state_empty(state: FSMContext) -> bool:
    """Check if state is empty"""
    if state:
        return len(state.get_data()) == 0
    return True

def validate_state_data(state: FSMContext, required_keys: list) -> bool:
    """Validate state data"""
    if not state:
        return False
    
    data = state.get_data()
    return all(key in data for key in required_keys)

def get_missing_state_keys(state: FSMContext, required_keys: list) -> list:
    """Get missing state keys"""
    if not state:
        return required_keys
    
    data = state.get_data()
    return [key for key in required_keys if key not in data]

def ensure_state_data(state: FSMContext, required_keys: list) -> None:
    """Ensure state data"""
    if not state:
        raise StateError("State context is not available")
    
    missing_keys = get_missing_state_keys(state, required_keys)
    if missing_keys:
        raise StateError(f"Missing required state keys: {missing_keys}")

def get_state_class(state: FSMContext) -> Optional[Type[BaseState]]:
    """Get state class"""
    if state:
        return state.get_state().group
    return None

def get_state_group(state: FSMContext) -> Optional[str]:
    """Get state group"""
    if state:
        state_class = state.get_state().group
        return state_class.__name__ if state_class else None
    return None

def get_state_group_states(state: FSMContext) -> Optional[list]:
    """Get state group states"""
    if state:
        state_class = state.get_state().group
        if state_class:
            return [state.state for state in state_class.states]
    return None

def is_state_in_group(state: FSMContext, group_name: str) -> bool:
    """Check if state is in group"""
    if state:
        state_group = get_state_group(state)
        return state_group == group_name
    return False

def get_state_group_state(state: FSMContext) -> Optional[str]:
    """Get state group state"""
    if state:
        return state.get_state().state
    return None

def set_state_group_state(state: FSMContext, new_state: State) -> None:
    """Set state group state"""
    if state:
        state.set_state(new_state)

def reset_state_group_state(state: FSMContext) -> None:
    """Reset state group state"""
    if state:
        state.finish()

def get_state_group_data(state: FSMContext) -> Dict[str, Any]:
    """Get state group data"""
    if state:
        return state.get_data()
    return {}

def set_state_group_data(state: FSMContext, data: Dict[str, Any]) -> None:
    """Set state group data"""
    if state:
        state.set_data(data)

def update_state_group_data(state: FSMContext, data: Dict[str, Any]) -> None:
    """Update state group data"""
    if state:
        current_data = state.get_data()
        current_data.update(data)
        state.set_data(current_data)

def clear_state_group_data(state: FSMContext) -> None:
    """Clear state group data"""
    if state:
        state.set_data({})

def get_state_group_value(state: FSMContext, key: str) -> Optional[Any]:
    """Get state group value"""
    if state:
        return state.get_data().get(key)
    return None

def set_state_group_value(state: FSMContext, key: str, value: Any) -> None:
    """Set state group value"""
    if state:
        data = state.get_data()
        data[key] = value
        state.set_data(data)

def remove_state_group_value(state: FSMContext, key: str) -> None:
    """Remove state group value"""
    if state:
        data = state.get_data()
        data.pop(key, None)
        state.set_data(data)

def has_state_group_value(state: FSMContext, key: str) -> bool:
    """Check if state group has value"""
    if state:
        return key in state.get_data()
    return False

def get_state_group_keys(state: FSMContext) -> list:
    """Get state group keys"""
    if state:
        return list(state.get_data().keys())
    return []

def get_state_group_values(state: FSMContext) -> list:
    """Get state group values"""
    if state:
        return list(state.get_data().values())
    return []

def get_state_group_items(state: FSMContext) -> list:
    """Get state group items"""
    if state:
        return list(state.get_data().items())
    return []

def get_state_group_length(state: FSMContext) -> int:
    """Get state group length"""
    if state:
        return len(state.get_data())
    return 0

def is_state_group_empty(state: FSMContext) -> bool:
    """Check if state group is empty"""
    if state:
        return len(state.get_data()) == 0
    return True

def validate_state_group_data(state: FSMContext, required_keys: list) -> bool:
    """Validate state group data"""
    if not state:
        return False
    
    data = state.get_data()
    return all(key in data for key in required_keys)

def get_missing_state_group_keys(state: FSMContext, required_keys: list) -> list:
    """Get missing state group keys"""
    if not state:
        return required_keys
    
    data = state.get_data()
    return [key for key in required_keys if key not in data]

def ensure_state_group_data(state: FSMContext, required_keys: list) -> None:
    """Ensure state group data"""
    if not state:
        raise StateError("State context is not available")
    
    missing_keys = get_missing_state_group_keys(state, required_keys)
    if missing_keys:
        raise StateError(f"Missing required state group keys: {missing_keys}")

async def set_state(
    state: FSMContext,
    state_name: str,
    data: Optional[dict[str, Any]] = None
) -> None:
    """Set state with optional data"""
    try:
        await state.set_state(state_name)
        if data:
            await state.update_data(**data)
    except Exception as e:
        raise StateError(f"Failed to set state: {str(e)}")

async def get_state_data(state: FSMContext) -> dict[str, Any]:
    """Get state data"""
    try:
        return await state.get_data()
    except Exception as e:
        raise StateError(f"Failed to get state data: {str(e)}")

async def update_state_data(
    state: FSMContext,
    data: dict[str, Any]
) -> None:
    """Update state data"""
    try:
        await state.update_data(**data)
    except Exception as e:
        raise StateError(f"Failed to update state data: {str(e)}")

async def clear_state(state: FSMContext) -> None:
    """Clear state and its data"""
    try:
        await state.finish()
    except Exception as e:
        raise StateError(f"Failed to clear state: {str(e)}")

async def get_current_state(state: FSMContext) -> Optional[str]:
    """Get current state name"""
    try:
        current_state = await state.get_state()
        return current_state
    except Exception as e:
        raise StateError(f"Failed to get current state: {str(e)}")

async def check_state(
    state: FSMContext,
    expected_state: str
) -> bool:
    """Check if current state matches expected state"""
    try:
        current_state = await state.get_state()
        return current_state == expected_state
    except Exception as e:
        raise StateError(f"Failed to check state: {str(e)}")

async def set_organization_state(
    state: FSMContext,
    org_id: int,
    org_name: str
) -> None:
    """Set organization state"""
    await set_state(
        state,
        "organization",
        {
            "org_id": org_id,
            "org_name": org_name
        }
    )

async def set_menu_state(
    state: FSMContext,
    org_id: int,
    file_path: str
) -> None:
    """Set menu state"""
    await set_state(
        state,
        "menu",
        {
            "org_id": org_id,
            "file_path": file_path
        }
    )

async def set_image_state(
    state: FSMContext,
    org_id: int,
    image_type: str,
    file_path: str
) -> None:
    """Set image state"""
    await set_state(
        state,
        "image",
        {
            "org_id": org_id,
            "image_type": image_type,
            "file_path": file_path
        }
    )

async def set_qr_code_state(
    state: FSMContext,
    org_id: int,
    qr_type: str
) -> None:
    """Set QR code state"""
    await set_state(
        state,
        "qr_code",
        {
            "org_id": org_id,
            "qr_type": qr_type
        }
    )

async def set_theme_state(
    state: FSMContext,
    org_id: int,
    theme_id: int
) -> None:
    """Set theme state"""
    await set_state(
        state,
        "theme",
        {
            "org_id": org_id,
            "theme_id": theme_id
        }
    )

async def set_web_page_state(
    state: FSMContext,
    org_id: int
) -> None:
    """Set web page state"""
    await set_state(
        state,
        "web_page",
        {
            "org_id": org_id
        }
    ) 