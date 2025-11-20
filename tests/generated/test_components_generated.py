"""
Auto-generated component validation tests
"""
import pytest
from sqlalchemy.orm import Session
from models.component import Component


def test_resistor_creation(db_session: Session):
    comp = Component(
        id="RESISTOR_TEST",
        type="resistor",
        value="1k",
        value_numeric=1000.0,
        unit="ohm",
        footprint="0805"
    )
    db_session.add(comp)
    db_session.commit()
    obj = db_session.query(Component).filter_by(id="RESISTOR_TEST").first()
    assert obj is not None


def test_capacitor_creation(db_session: Session):
    comp = Component(
        id="CAPACITOR_TEST",
        type="capacitor",
        value="1k",
        value_numeric=1000.0,
        unit="ohm",
        footprint="0805"
    )
    db_session.add(comp)
    db_session.commit()
    obj = db_session.query(Component).filter_by(id="CAPACITOR_TEST").first()
    assert obj is not None


def test_inductor_creation(db_session: Session):
    comp = Component(
        id="INDUCTOR_TEST",
        type="inductor",
        value="1k",
        value_numeric=1000.0,
        unit="ohm",
        footprint="0805"
    )
    db_session.add(comp)
    db_session.commit()
    obj = db_session.query(Component).filter_by(id="INDUCTOR_TEST").first()
    assert obj is not None


def test_diode_creation(db_session: Session):
    comp = Component(
        id="DIODE_TEST",
        type="diode",
        value="1k",
        value_numeric=1000.0,
        unit="ohm",
        footprint="0805"
    )
    db_session.add(comp)
    db_session.commit()
    obj = db_session.query(Component).filter_by(id="DIODE_TEST").first()
    assert obj is not None
