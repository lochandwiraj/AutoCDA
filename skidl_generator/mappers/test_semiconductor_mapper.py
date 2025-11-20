from semiconductor_components import SemiconductorMapper

def run_tests():
    mapper = SemiconductorMapper()

    # test diode
    d1 = mapper.create_diode({
        "id": "D1",
        "part_number": "1N4148"
    })
    print(f"? Diode created: {d1.ref} = {d1.value}")

    # test NPN transistor
    q1 = mapper.create_transistor({
        "id": "Q1",
        "part_number": "2N2222"
    })
    print(f"? NPN created: {q1.ref} symbol={q1.name}")

    # test PNP transistor
    q2 = mapper.create_transistor({
        "id": "Q2",
        "part_number": "2N3906"
    })
    print(f"? PNP created: {q2.ref} symbol={q2.name}")

if __name__ == "__main__":
    run_tests()
