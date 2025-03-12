from drone_mode import DroneMode
import math

def test_drone_mode():
    drone_mode = DroneMode(start_gui=False)

    # apds_light_to_midi
    assert drone_mode.apds_light_to_midi(0) == 20, "Zero test failed"
    assert drone_mode.apds_light_to_midi(65535) == 108, "Max test failed"
    assert drone_mode.apds_light_to_midi(32767) == 63, "Mid test failed"
    assert drone_mode.apds_light_to_midi(32767.5) == 64, "Non-integer test failed"

    # mirror_midi
    assert drone_mode.invert_midi(28) == 100, "Mirroring failed"
    assert drone_mode.invert_midi(108) == 20, "Mirroring failed"
    assert drone_mode.invert_midi(20) == 108, "Mirroring failed"

    # lfo generators
    assert drone_mode.apds_light_to_low_freq(0) == 1, "Zero test failed"
    assert drone_mode.apds_light_to_low_freq(65535) == 20, "Max test failed"
    assert drone_mode.apds_light_to_low_freq(32767) == 10, "Mid test failed"

    ## set theory - converting to pitch and interval classes

    # mido to pitch class
    assert drone_mode.midi_to_pitch_class(60) == 0, "C to 0 test failed"
    assert drone_mode.midi_to_pitch_class(49) == 1, "D to 1 test failed"
    assert drone_mode.midi_to_pitch_class(72) == 0, "C to 0 test failed"
    assert drone_mode.midi_to_pitch_class(77) == 5, "Whatever 77 is to 5 test failed"

    # invert pitch class
    assert drone_mode.invert_pitch_class(0) == 0, "Invert 0 test failed" # 0 inverts to itself
    assert drone_mode.invert_pitch_class(6) == 6, "Invert 6 test failed" # 6 inverts to itself
    assert drone_mode.invert_pitch_class(5) == 7, "Invert 5 test failed"
    assert drone_mode.invert_pitch_class(1) == 11, "Invert 1 test failed"

    # find interval class
    assert drone_mode.find_interval_class(0, 1) == 1, "Interval class 1 failed (0, 1)"
    assert drone_mode.find_interval_class(1, 0) == 1, "Interval class 1 failed (1, 0)"
    assert drone_mode.find_interval_class(2, 1) == 1, "Interval class 1 failed (2, 1)"
    assert drone_mode.find_interval_class(11, 2) == 3, "Interval class 3 failed (11, 2)"
    assert drone_mode.find_interval_class(2, 11) == 3, "Interval class 3 failed (11, 2)"
    assert drone_mode.find_interval_class(0, 7) == 5, "Interval class 5 failed (0, 7)"

    # light to tremolo
    assert drone_mode.apds_light_to_tremolo(0) == 0.001, "Floor tremolo test failed"
    assert drone_mode.apds_light_to_tremolo(65535) == 0.1, "Ceiling tremolo test failed"
    assert drone_mode.apds_light_to_tremolo(32767.5) == 0.0505, "Midpoint tremolo test failed"

    # light to radians
    assert drone_mode.apds_light_to_radians(0) == 0, "Radians floor test failed"
    assert drone_mode.apds_light_to_radians(65535) == 2 * math.pi, "Radians ceiling test failed"
    assert drone_mode.apds_light_to_radians(32767.5) == math.pi, "Midpoint test failed"



    print("All tests passed!")

# when python runs a file directly, it assigns the value "__main__" to __name__ for that file
# if this is imported to another file and runs, __name__ will be assigned to the name of the name of the module
if __name__ == "__main__":
    # Run the tests
    test_drone_mode()