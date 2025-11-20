# --------------------------------------------------------
# conftest.py  (FULL WORKING VERSION)
# Provides:
#   - SQLAlchemy Base
#   - Component model
#   - In-memory SQLite DB session fixture for pytest
# --------------------------------------------------------

import pytest
from sqlalchemy import create_engine, Column, String, Float, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------
# SQLAlchemy Base
# --------------------------------------
Base = declarative_base()

# --------------------------------------
# Component Model (matches your system)
# --------------------------------------
class Component(Base):
    __tablename__ = "components"

    id = Column(String, primary_key=True)
    type = Column(String, index=True)
    value = Column(String)
    value_numeric = Column(Float)
    unit = Column(String)
    tolerance = Column(String, nullable=True)
    footprint = Column(String)
    datasheet_url = Column(String, nullable=True)
    properties = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Component {self.id}: {self.value}>"

# --------------------------------------
# PYTEST FIXTURE — In-memory DB
# --------------------------------------
@pytest.fixture
def db_session():
    """
    Creates a temporary in-memory SQLite database
    for component creation tests.
    AutoCDA tests expect this fixture.
    """
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Create tables fresh for each test
    Base.metadata.create_all(engine)

    session = TestingSession()

    try:
        yield session
    finally:
        session.close()
