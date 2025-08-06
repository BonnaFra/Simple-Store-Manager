# seed.py
from sqlmodel import SQLModel, Session, create_engine
import psycopg2
from datetime import datetime, timedelta
from models import *
from credentials import DB_CREDENTIALS, DB_NAME # Importa le credenziali

# Connection string per il database predefinito
default_connection_params = DB_CREDENTIALS

# Crea il database gb_magazzino
conn = psycopg2.connect(**default_connection_params)
conn.autocommit = True  # Necessario per creare un nuovo database
cur = conn.cursor()
cur.execute("CREATE DATABASE gb_magazzino WITH OWNER postgres ENCODING 'UTF8'")
cur.close()
conn.close()

# Connection string per il database gb_magazzino
url = f"postgresql+psycopg2://{DB_CREDENTIALS['user']}:{DB_CREDENTIALS['password']}@{DB_CREDENTIALS['host']}:{DB_CREDENTIALS['port']}/{DB_NAME}"
engine = create_engine(url)

def seed_data():
    # Crea tutte le tabelle definite in models.py
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Components
        o_ring = Component(sku="O-RING", name="O-RING", kind=ComponentKind.RAW)
        molla = Component(sku="MOLLA", name="MOLLA", kind=ComponentKind.RAW)
        magnete = Component(sku="MAGNETE", name="MAGNETE", kind=ComponentKind.RAW)
        ampolla_read = Component(sku="AMPOLLA_READ", name="AMPOLLA READ", kind=ComponentKind.RAW)
        involucro_pedalina = Component(sku="INVOLUCRO_PEDALINA", name="INVOLUCRO PEDALINA", kind=ComponentKind.RAW)
        pedalina = Component(sku="PED-STD", name="PEDALINA", kind=ComponentKind.ASSEMBLY, qr_code="PED-STD")
        board_std = Component(sku="BOARD-STD", name="BOARD", kind=ComponentKind.ASSEMBLY, qr_code="BOARD-STD")
        case_board = Component(sku="CASE-BOARD", name="CASE", kind=ComponentKind.ASSEMBLY, qr_code="CASE-BOARD")
        conn_3pin_yam = Component(sku="CONN-3PIN-YAM", name="Connector 3PIN YAM", kind=ComponentKind.ASSEMBLY, qr_code="CONN-3PIN-YAM")
        conn_4pin_duc = Component(sku="CONN-4PIN-DUC", name="Connector 4PIN DUC", kind=ComponentKind.ASSEMBLY, qr_code="CONN-4PIN-DUC")
        conn_2pin_ktm = Component(sku="CONN-2PIN-KTM", name="Connector 2PIN KTM", kind=ComponentKind.ASSEMBLY, qr_code="CONN-2PIN-KTM")
        session.add_all([o_ring, molla, magnete, ampolla_read, involucro_pedalina, pedalina, board_std, case_board, conn_3pin_yam, conn_4pin_duc, conn_2pin_ktm])

        # BOM for PEDALINA
        session.add_all([
            ComponentPart(assembly_id=pedalina.id, part_id=o_ring.id, qty=1),
            ComponentPart(assembly_id=pedalina.id, part_id=molla.id, qty=1),
            ComponentPart(assembly_id=pedalina.id, part_id=magnete.id, qty=1),
            ComponentPart(assembly_id=pedalina.id, part_id=ampolla_read.id, qty=1),
            ComponentPart(assembly_id=pedalina.id, part_id=involucro_pedalina.id, qty=1),
        ])

        # Supplier
        supplier = Supplier(name="MechaParts Srl", email="info@mechaparts.com", phone="123456789")
        session.add(supplier)
        session.commit()  # Commit necessario per salvare il fornitore nel database

        # Delivery
        delivery = Delivery(
            supplier_id=supplier.id,  # Usa l'ID del fornitore appena salvato
            order_date=datetime.utcnow() - timedelta(days=30),
            received_date=datetime.utcnow(),
            has_issues=False,
            notes="Initial stock delivery"
        )
        session.add(delivery)

        # Delivery lines
        session.add_all([
            DeliveryLine(delivery_id=delivery.id, component_id=o_ring.id, qty_ordered=50, qty_received=50),
            DeliveryLine(delivery_id=delivery.id, component_id=molla.id, qty_ordered=50, qty_received=50),
        ])

        # Stock
        for component in [o_ring, molla, magnete, ampolla_read, involucro_pedalina, pedalina, board_std, case_board, conn_3pin_yam, conn_4pin_duc, conn_2pin_ktm]:
            session.add(Stock(component_id=component.id, qty_available=100))

        # Shopify Order
        order = Order(
            shopify_id=1234567890,
            created_at_shop=datetime.utcnow(),
            status=OrderStatus.PENDING,
            customer_name="Mario Rossi"
        )
        session.add(order)

        # Order lines
        session.add_all([
            OrderLine(order_id=order.id, component_id=pedalina.id, qty=1),
            OrderLine(order_id=order.id, component_id=conn_3pin_yam.id, qty=1),
            OrderLine(order_id=order.id, component_id=board_std.id, qty=1),
        ])

        session.commit()
        print("Seed completed. Check your database in pgAdmin4.")

if __name__ == "__main__":
    seed_data()