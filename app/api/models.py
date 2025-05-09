# app/models.py
from database import Base, get_db
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, BigInteger, ForeignKey
from datetime import datetime, UTC
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

@dataclass
class MenuTable:
    """Dataclass for defining menu table structure"""
    __tablename__: str = "menu"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    name: Column = Column(String, nullable=False)
    description: Column = Column(String, nullable=True)
    price: Column = Column(Numeric, nullable=False)
    category: Column = Column(String, nullable=False)
    subcategory: Column = Column(String, nullable=True)
    is_available: Column = Column(Boolean, default=True)
    image_url: Column = Column(String, nullable=True)
    created_at: Column = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Column = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

@dataclass
class MenuData:
    """Dataclass for menu data operations"""
    name: str
    price: Decimal
    category: str
    description: Optional[str] = None
    subcategory: Optional[str] = None
    is_available: bool = True
    image_url: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "category": self.category,
            "subcategory": self.subcategory,
            "is_available": self.is_available,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuData':
        return cls(
            id=data.get('id'),
            name=data['name'],
            description=data.get('description'),
            price=Decimal(str(data['price'])),
            category=data['category'],
            subcategory=data.get('subcategory'),
            is_available=data.get('is_available', True),
            image_url=data.get('image_url'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )

class Menu(Base):
    """SQLAlchemy model for menu table"""
    __tablename__ = MenuTable.__tablename__

    id = MenuTable.id
    name = MenuTable.name
    description = MenuTable.description
    price = MenuTable.price
    category = MenuTable.category
    subcategory = MenuTable.subcategory
    is_available = MenuTable.is_available
    image_url = MenuTable.image_url
    created_at = MenuTable.created_at
    updated_at = MenuTable.updated_at

    def to_dataclass(self) -> MenuData:
        return MenuData(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            category=self.category,
            subcategory=self.subcategory,
            is_available=self.is_available,
            image_url=self.image_url,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_dataclass(cls, data: MenuData) -> 'Menu':
        return cls(
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category,
            subcategory=data.subcategory,
            is_available=data.is_available,
            image_url=data.image_url
        )

    @classmethod
    def create(cls, db: Session, menu_data: MenuData) -> 'Menu':
        """Create new menu item"""
        try:
            menu = cls.from_dataclass(menu_data)
            db.add(menu)
            db.commit()
            db.refresh(menu)
            return menu
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def get_by_id(cls, db: Session, menu_id: int) -> Optional['Menu']:
        """Get menu item by ID"""
        return db.query(cls).filter(cls.id == menu_id).first()

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List['Menu']:
        """Get all menu items with pagination"""
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def update(cls, db: Session, menu_id: int, menu_data: MenuData) -> Optional['Menu']:
        """Update menu item"""
        try:
            menu = cls.get_by_id(db, menu_id)
            if menu:
                for key, value in menu_data.__dict__.items():
                    if key != 'id' and value is not None:
                        setattr(menu, key, value)
                db.commit()
                db.refresh(menu)
            return menu
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def delete(cls, db: Session, menu_id: int) -> bool:
        """Delete menu item"""
        try:
            menu = cls.get_by_id(db, menu_id)
            if menu:
                db.delete(menu)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise e

@dataclass
class MainTable:
    """Dataclass for defining main table structure"""
    __tablename__: str = "main"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    name: Column = Column(String, nullable=False)
    owner: Column = Column(String, nullable=False)
    name_menu_table: Column = Column(String, nullable=False)
    created: Column = Column(DateTime, default=lambda: datetime.now(UTC))

@dataclass
class MainData:
    """Dataclass for main data operations"""
    name: str
    owner: str
    name_menu_table: str
    id: Optional[int] = None
    created: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "name_menu_table": self.name_menu_table,
            "created": self.created.isoformat() if self.created else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MainData':
        return cls(
            id=data.get('id'),
            name=data['name'],
            owner=data['owner'],
            name_menu_table=data['name_menu_table'],
            created=datetime.fromisoformat(data['created']) if data.get('created') else None
        )

class Main(Base):
    """SQLAlchemy model for main table"""
    __tablename__ = MainTable.__tablename__

    id = MainTable.id
    name = MainTable.name
    owner = MainTable.owner
    name_menu_table = MainTable.name_menu_table
    created = MainTable.created

    def to_dataclass(self) -> MainData:
        return MainData(
            id=self.id,
            name=self.name,
            owner=self.owner,
            name_menu_table=self.name_menu_table,
            created=self.created
        )

    @classmethod
    def from_dataclass(cls, data: MainData) -> 'Main':
        return cls(
            name=data.name,
            owner=data.owner,
            name_menu_table=data.name_menu_table
        )

    @classmethod
    def create(cls, db: Session, main_data: MainData) -> 'Main':
        """Create new main item"""
        try:
            main = cls.from_dataclass(main_data)
            db.add(main)
            db.commit()
            db.refresh(main)
            return main
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def get_by_id(cls, db: Session, main_id: int) -> Optional['Main']:
        """Get main item by ID"""
        return db.query(cls).filter(cls.id == main_id).first()

    @classmethod
    def get_by_owner(cls, db: Session, owner: str) -> List['Main']:
        """Get main items by owner"""
        return db.query(cls).filter(cls.owner == owner).all()

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List['Main']:
        """Get all main items with pagination"""
        return db.query(cls).offset(skip).limit(limit).all()

@dataclass
class UserTable:
    """Dataclass for defining users table structure"""
    __tablename__: str = "users"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    tid: Column = Column(BigInteger, nullable=False)
    owner: Column = Column(Boolean, default=False)
    language: Column = Column(String, default='ru')
    created: Column = Column(DateTime, default=lambda: datetime.now(UTC))
    updated: Column = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

@dataclass
class UserData:
    """Dataclass for user data operations"""
    tid: int
    owner: bool = False
    id: Optional[int] = None
    language: str = 'ru'
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tid": self.tid,
            "owner": self.owner,
            "language": self.language,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserData':
        return cls(
            id=data.get('id'),
            tid=data['tid'],
            owner=data.get('owner', False),
            language=data.get('language', 'ru'),
            created=datetime.fromisoformat(data['created']) if data.get('created') else None,
            updated=datetime.fromisoformat(data['updated']) if data.get('updated') else None
        )

class User(Base):
    """SQLAlchemy model for users table"""
    __tablename__ = UserTable.__tablename__

    id = UserTable.id
    tid = UserTable.tid
    owner = UserTable.owner
    language = UserTable.language
    created = UserTable.created
    updated = UserTable.updated

    def to_dataclass(self) -> UserData:
        return UserData(
            id=self.id,
            tid=self.tid,
            owner=self.owner,
            language=self.language,
            created=self.created,
            updated=self.updated
        )

    @classmethod
    def from_dataclass(cls, data: UserData) -> 'User':
        return cls(
            tid=data.tid,
            owner=data.owner,
            language=data.language
        )

    @classmethod
    def create(cls, db: Session, user_data: UserData) -> 'User':
        """Create new user"""
        try:
            user = cls.from_dataclass(user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> Optional['User']:
        """Get user by ID"""
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_by_tid(cls, db: Session, tid: int) -> Optional['User']:
        """Get user by Telegram ID"""
        return db.query(cls).filter(cls.tid == tid).first()

    @classmethod
    def get_owners(cls, db: Session) -> List['User']:
        """Get all owner users"""
        return db.query(cls).filter(cls.owner == True).all()

@dataclass
class OrganizationTable:
    """Dataclass for defining organizations table structure"""
    __tablename__: str = "organizations"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    name: Column = Column(String, nullable=False)
    description: Column = Column(String, nullable=True)
    owner_id: Column = Column(Integer, ForeignKey("users.id"), nullable=False)
    menu_table_name: Column = Column(String, nullable=False)
    created: Column = Column(DateTime, default=lambda: datetime.now(UTC))
    updated: Column = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

@dataclass
class OrganizationData:
    """Dataclass for organization data operations"""
    name: str
    description: Optional[str] = None
    owner_id: Optional[int] = None
    menu_table_name: Optional[str] = None
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "menu_table_name": self.menu_table_name,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrganizationData':
        return cls(
            id=data.get('id'),
            name=data['name'],
            description=data.get('description'),
            owner_id=data.get('owner_id'),
            menu_table_name=data.get('menu_table_name'),
            created=datetime.fromisoformat(data['created']) if data.get('created') else None,
            updated=datetime.fromisoformat(data['updated']) if data.get('updated') else None
        )

class Organization(Base):
    """SQLAlchemy model for organizations table"""
    __tablename__ = OrganizationTable.__tablename__

    id = OrganizationTable.id
    name = OrganizationTable.name
    description = OrganizationTable.description
    owner_id = OrganizationTable.owner_id
    menu_table_name = OrganizationTable.menu_table_name
    created = OrganizationTable.created
    updated = OrganizationTable.updated

    def to_dataclass(self) -> OrganizationData:
        return OrganizationData(
            id=self.id,
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            menu_table_name=self.menu_table_name,
            created=self.created,
            updated=self.updated
        )

    @classmethod
    def from_dataclass(cls, data: OrganizationData) -> 'Organization':
        return cls(
            name=data.name,
            description=data.description,
            owner_id=data.owner_id,
            menu_table_name=data.menu_table_name
        )

    @classmethod
    def create(cls, db: Session, org_data: OrganizationData) -> 'Organization':
        """Create new organization"""
        try:
            org = cls.from_dataclass(org_data)
            db.add(org)
            db.commit()
            db.refresh(org)
            return org
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def get_by_id(cls, db: Session, org_id: int) -> Optional['Organization']:
        """Get organization by ID"""
        return db.query(cls).filter(cls.id == org_id).first()

    @classmethod
    def get_by_owner(cls, db: Session, owner_id: int) -> List['Organization']:
        """Get organizations by owner"""
        return db.query(cls).filter(cls.owner_id == owner_id).all()

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List['Organization']:
        """Get all organizations with pagination"""
        return db.query(cls).offset(skip).limit(limit).all()

@dataclass
class MenuItemTable:
    """Dataclass for defining menu items table structure"""
    __tablename__: str = "menu_items"
    
    id: Column = Column(Integer, primary_key=True, index=True)
    organization_id: Column = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name: Column = Column(String, nullable=False)
    description: Column = Column(String, nullable=True)
    price: Column = Column(Numeric, nullable=False)
    category: Column = Column(String, nullable=False)
    subcategory: Column = Column(String, nullable=True)
    is_available: Column = Column(Boolean, default=True)
    image_url: Column = Column(String, nullable=True)
    created_at: Column = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Column = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

@dataclass
class MenuItemData:
    """Dataclass for menu item data operations"""
    organization_id: int
    name: str
    price: Decimal
    category: str
    description: Optional[str] = None
    subcategory: Optional[str] = None
    is_available: bool = True
    image_url: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "category": self.category,
            "subcategory": self.subcategory,
            "is_available": self.is_available,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MenuItemData':
        return cls(
            id=data.get('id'),
            organization_id=data['organization_id'],
            name=data['name'],
            description=data.get('description'),
            price=Decimal(str(data['price'])),
            category=data['category'],
            subcategory=data.get('subcategory'),
            is_available=data.get('is_available', True),
            image_url=data.get('image_url'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )

class MenuItem(Base):
    """SQLAlchemy model for menu items table"""
    __tablename__ = MenuItemTable.__tablename__

    id = MenuItemTable.id
    organization_id = MenuItemTable.organization_id
    name = MenuItemTable.name
    description = MenuItemTable.description
    price = MenuItemTable.price
    category = MenuItemTable.category
    subcategory = MenuItemTable.subcategory
    is_available = MenuItemTable.is_available
    image_url = MenuItemTable.image_url
    created_at = MenuItemTable.created_at
    updated_at = MenuItemTable.updated_at

    def to_dataclass(self) -> MenuItemData:
        return MenuItemData(
            id=self.id,
            organization_id=self.organization_id,
            name=self.name,
            description=self.description,
            price=self.price,
            category=self.category,
            subcategory=self.subcategory,
            is_available=self.is_available,
            image_url=self.image_url,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_dataclass(cls, data: MenuItemData) -> 'MenuItem':
        return cls(
            organization_id=data.organization_id,
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category,
            subcategory=data.subcategory,
            is_available=data.is_available,
            image_url=data.image_url
        )

    @classmethod
    def create(cls, db: Session, menu_item_data: MenuItemData) -> 'MenuItem':
        """Create new menu item"""
        try:
            menu_item = cls.from_dataclass(menu_item_data)
            db.add(menu_item)
            db.commit()
            db.refresh(menu_item)
            return menu_item
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def get_by_id(cls, db: Session, menu_item_id: int) -> Optional['MenuItem']:
        """Get menu item by ID"""
        return db.query(cls).filter(cls.id == menu_item_id).first()

    @classmethod
    def get_by_organization(cls, db: Session, organization_id: int) -> List['MenuItem']:
        """Get menu items by organization"""
        return db.query(cls).filter(cls.organization_id == organization_id).all()

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List['MenuItem']:
        """Get all menu items with pagination"""
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def update(cls, db: Session, menu_item_id: int, menu_item_data: MenuItemData) -> Optional['MenuItem']:
        """Update menu item"""
        try:
            menu_item = cls.get_by_id(db, menu_item_id)
            if menu_item:
                for key, value in menu_item_data.__dict__.items():
                    if key != 'id' and value is not None:
                        setattr(menu_item, key, value)
                db.commit()
                db.refresh(menu_item)
            return menu_item
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @classmethod
    def delete(cls, db: Session, menu_item_id: int) -> bool:
        """Delete menu item"""
        try:
            menu_item = cls.get_by_id(db, menu_item_id)
            if menu_item:
                db.delete(menu_item)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise e

