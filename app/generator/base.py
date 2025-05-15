from dataclasses import dataclass
from typing import Dict, List, Any



# @dataclass
# class Dish:
#     name: str
#     price: float
#     description: str
#     subcategory: str

@dataclass
class PageData:
    page_name: str
    title: str
    description: str
    theme: str
    content: Dict[str, Any] 