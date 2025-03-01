from utils import DroneUtils

def test_drone_utils():
    utils = DroneUtils()

    assert utils.apds_light_to_midi(0) == 20, "Zero test failed"
    assert utils.apds_light_to_midi(65535) == 108, "Max value test failed"
    assert utils.apds_light_to_midi(32767) == 63, "Middle value test failed"
    assert utils.apds_light_to_midi(32767.5) == 64, "Non-integer test failed"

    assert utils.flip_midi(28) == 100, "Flipping failed"
    assert utils.flip_midi(108) == 20, "Flipping failed"
    assert utils.flip_midi(20) == 108, "Flipping failed"
    
    print("All tests passed!")

# Run the tests
test_drone_utils()