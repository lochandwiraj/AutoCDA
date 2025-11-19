from integration.pipeline import SKiDLPipeline

def test_rc_filter_pipeline():
    pipeline = SKiDLPipeline()

    dsl = {
        "components": [
            {"type": "resistor", "id": "R1", "value": "1k", "nets": ["VIN", "N001"]},
            {"type": "capacitor", "id": "C1", "value": "159n", "nets": ["N001", "GND"]}
        ],
        "constraints": {"cutoff": "1kHz"}
    }

    result = pipeline.generate_from_dsl(dsl)

    assert result["success"], f"Pipeline failed: {result.get('error')}"
    assert "R1" in result["skidl_code"]
    assert "C1" in result["skidl_code"]
    assert len(result["parsed"]["components"]) == 2

    print("✓ Full pipeline test passed!")

if __name__ == "__main__":
    test_rc_filter_pipeline()


