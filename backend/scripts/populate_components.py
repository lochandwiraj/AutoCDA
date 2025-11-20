import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.component import Component, Base

def load_components():
    engine = create_engine('sqlite:///autocda.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    with open('data/standard_components.json') as f:
        data = json.load(f)
    
    for comp_data in data['components']:
        comp = Component(**comp_data)
        session.merge(comp)  # upsert
    
    session.commit()
    print(f"Loaded {len(data['components'])} components")

if __name__ == "__main__":
    load_components()