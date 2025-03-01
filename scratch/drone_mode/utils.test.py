from utils import DroneUtils

def test_drone_utils():
    utils = DroneUtils()

    # apds_light_to_midi
    assert utils.apds_light_to_midi(0) == 20, "Zero test failed"
    assert utils.apds_light_to_midi(65535) == 108, "Max test failed"
    assert utils.apds_light_to_midi(32767) == 63, "Mid test failed"
    assert utils.apds_light_to_midi(32767.5) == 64, "Non-integer test failed"

    # mirror_midi
    assert utils.mirror_midi(28) == 100, "Mirroring failed"
    assert utils.mirror_midi(108) == 20, "Mirroring failed"
    assert utils.mirror_midi(20) == 108, "Mirroring failed"

    # 
    assert utils.apds_light_to_low_freq(0) == 1, "Zero test failed"
    assert utils.apds_light_to_low_freq(65535) == 20, "Max test failed"
    assert utils.apds_light_to_low_freq(32767) == 10, "Mid test failed"

    print("All tests passed!")

# Run the tests
test_drone_utils()