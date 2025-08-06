# models.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from enum import Enum
from datetime import datetime

class ComponentKind(str, Enum):
    RAW = "RAW"
    ASSEMBLY = "ASSEMBLY"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_PICK = "IN_PICK"
    PREPARED = "PREPARED"

class MovementSource(str, Enum):
    ORDER = "ORDER"
    DELIVERY = "DELIVERY"
    MANUAL = "MANUAL"

class Role(str, Enum):
    WAREHOUSE = "WAREHOUSE"
    ADMIN = "ADMIN"

class Component(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    sku: str = Field(unique=True)
    name: str
    qr_code: str | None = Field(default=None, unique=True)
    kind: ComponentKind
    unit: str = Field(default="pcs")
    parts: list["ComponentPart"] = Relationship(
        back_populates="assembly",
        sa_relationship_kwargs={"foreign_keys": "ComponentPart.assembly_id"}
    )
    parent_of: list["ComponentPart"] = Relationship(
        back_populates="part",
        sa_relationship_kwargs={"foreign_keys": "ComponentPart.part_id"}
    )
    stock: "Stock" = Relationship(
        back_populates="component",
        sa_relationship_kwargs={"uselist": False}
    )
    inventory_movements: list["InventoryMovement"] = Relationship(
        back_populates="component"
    )

class ComponentPart(SQLModel, table=True):
    assembly_id: str = Field(foreign_key="component.id", primary_key=True)
    part_id: str = Field(foreign_key="component.id", primary_key=True)
    qty: int
    assembly: Component = Relationship(
        back_populates="parts",
        sa_relationship_kwargs={"foreign_keys": "ComponentPart.assembly_id"}
    )
    part: Component = Relationship(
        back_populates="parent_of",
        sa_relationship_kwargs={"foreign_keys": "ComponentPart.part_id"}
    )

class Stock(SQLModel, table=True):
    component_id: str = Field(foreign_key="component.id", primary_key=True)
    qty_available: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    component: Component = Relationship(back_populates="stock")

class Supplier(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    email: str
    phone: str

class Delivery(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    supplier_id: str = Field(foreign_key="supplier.id")
    order_date: datetime
    received_date: datetime | None = None
    has_issues: bool
    notes: str | None = None
    lines: list["DeliveryLine"] = Relationship(back_populates="delivery", sa_relationship_kwargs={"cascade": "all, delete"})

class DeliveryLine(SQLModel, table=True):
    delivery_id: str = Field(foreign_key="delivery.id", primary_key=True)
    component_id: str = Field(foreign_key="component.id", primary_key=True)
    qty_ordered: int
    qty_received: int
    delivery: Delivery = Relationship(back_populates="lines")

class Order(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    shopify_id: int
    created_at_shop: datetime
    prepared_at: datetime | None = None
    status: OrderStatus
    customer_name: str
    lines: list["OrderLine"] = Relationship(back_populates="order", sa_relationship_kwargs={"cascade": "all, delete"})

class OrderLine(SQLModel, table=True):
    order_id: str = Field(foreign_key="order.id", primary_key=True)
    component_id: str = Field(foreign_key="component.id", primary_key=True)
    qty: int
    order: Order = Relationship(back_populates="lines")

class InventoryMovement(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    component_id: str = Field(foreign_key="component.id")
    delta: int
    source_type: MovementSource
    source_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    component: Component = Relationship(back_populates="inventory_movements")

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    username: str = Field(unique=True)
    password_hash: str
    role: Role