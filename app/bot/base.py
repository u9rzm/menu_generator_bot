from dataclasses import dataclass
from typing import Dict, List



@dataclass
class Dish:
    name: str
    price: float
    description: str

@dataclass
class PageData:
    page_name: str
    title: str
    theme: str
    content: Dict[str, List[Dish]] 