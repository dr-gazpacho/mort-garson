class DroneUtils():

    def __init__(self):
        self.APDS_MAX = 65535


    # where a 0 read from APDS correlates to 20 on midi, 65535 correlates to 108
    # greater quantitiy of light = higher frequency tone
    def apds_light_to_midi(self, apds_reading):
        return int(apds_reading * 88 / self.APDS_MAX) + 20
    
    # use in conjunction with apds_light_to_midi, would give opposite effect
    # this will likely be useless
    def flip_midi(self, midi_value):
        return 108 - midi_value + 20