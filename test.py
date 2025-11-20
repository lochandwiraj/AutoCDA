from app.core.database import SessionLocal
from app.models.circuit import CircuitDesign

def test_create_design():
    db = SessionLocal()

    # Create test design
    design = CircuitDesign(
        description="Test RC filter",
        constraints={"cutoff": "1kHz"},
        status="pending"
    )

    db.add(design)
    db.commit()
    db.refresh(design)

    print("Created Design:")
    print("ID:", design.id)
    print("Description:", design.description)
    print("Constraints:", design.constraints)
    print("Status:", design.status)

    # Read back from DB
    stored = db.query(CircuitDesign).filter(CircuitDesign.id == design.id).first()
    print("\nFetched from DB:")
    print("ID:", stored.id)
    print("Description:", stored.description)
    print("Constraints:", stored.constraints)
    print("Status:", stored.status)


if __name__ == "__main__":
    test_create_design()
