from active_components import ActiveMapper

def run_tests():
    mapper = ActiveMapper()

    opamp = mapper.create_opamp({
        "id": "U1",
        "type": "LM741",
        "connections": {"IN+":"VIN", "IN-":"GND", "OUT":"VOUT"}
    })
    print(f"? OpAmp created: {opamp.ref}")

    ic555 = mapper.create_555({
        "id": "U2",
        "type": "NE555P",
        "connections": {}
    })
    print(f"? 555 created: {ic555.ref}")

if __name__ == "__main__":
    run_tests()
