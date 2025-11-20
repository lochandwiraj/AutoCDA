# scripts/init_db.py
from app.database import init_db, SessionLocal
from app.models import Component
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime

def seed_components():
    db = SessionLocal()
    common = [
        {"name": "R_1k", "type": "resistor", "parameters": {"value": "1k", "tolerance": "5%"}, "footprint": "Resistor_SMD:R_0805_2012Metric"},
        {"name": "C_100n", "type": "capacitor", "parameters": {"value": "100n", "voltage": "50V"}, "footprint": "Capacitor_SMD:C_0805_2012Metric"},
        {"name": "LM741", "type": "ic_opamp", "parameters": {"type": "opamp", "channels": 1}, "footprint": "Package_DIP:DIP-8_W7.62mm"},
        {"name": "1N4148", "type": "diode", "parameters": {"type": "signal", "voltage": "100V"}, "footprint": "Diode_SMD:D_SOD-123"},
    ]

    for c in common:
        stmt = (
            insert(Component)
            .values(
                name=c["name"],
                type=c["type"],
                parameters=c["parameters"],
                footprint=c["footprint"],
                in_stock=True,
                created_at=datetime.utcnow(),
            )
            .on_conflict_do_nothing(index_elements=["name"])
        )
        db.execute(stmt)

    db.commit()
    db.close()
    print("✅ Components seeded (idempotent).")

if __name__ == "__main__":
    print("Initializing database…")
    init_db()
    print("Seeding components…")
    seed_components()
