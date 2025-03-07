from drone_mode import DroneMode

def test_drone_mode():
    drone_mode = DroneMode(start_gui=False)

    # apds_light_to_midi
    assert drone_mode.apds_light_to_midi(0) == 20, "Zero test failed"
    assert drone_mode.apds_light_to_midi(65535) == 108, "Max test failed"
    assert drone_mode.apds_light_to_midi(32767) == 63, "Mid test failed"
    assert drone_mode.apds_light_to_midi(32767.5) == 64, "Non-integer test failed"

    # mirror_midi
    assert drone_mode.mirror_midi(28) == 100, "Mirroring failed"
    assert drone_mode.mirror_midi(108) == 20, "Mirroring failed"
    assert drone_mode.mirror_midi(20) == 108, "Mirroring failed"

    # 
    assert drone_mode.apds_light_to_low_freq(0) == 1, "Zero test failed"
    assert drone_mode.apds_light_to_low_freq(65535) == 20, "Max test failed"
    assert drone_mode.apds_light_to_low_freq(32767) == 10, "Mid test failed"

    print("All tests passed!")

# when python runs a file directly, it assigns the value "__main__" to __name__ for that file
# if this is imported to another file and runs, __name__ will be assigned to the name of the name of the module
if __name__ == "__main__":
    # Run the tests
    test_drone_mode()