class DroneUtils():

    def __init__(self):
        self.APDS_MAX = 65535


    # where a 0 read from APDS correlates to 20 on midi, 65535 correlates to 108
    # greater quantitiy of light = higher frequency tone
    def apds_light_to_midi(self, apds_reading):
        """
        Convert APDS values to MIDI;
        Floor: 20, Ceiling: 108;
        APDS_MIN -> 20, APDS_MAX -> 108
        """
        return int(apds_reading * 88 / self.APDS_MAX) + 20
    
    def mirror_midi(self, midi_value):
        """Mirrors MIDI; 40 -> 88, 20 -> 108"""
        return 128 - midi_value
    
    def apds_light_to_low_freq(self, apds_reading):
        """
        Convert APDS values to LFO values;
        Floor: 1, Ceiling: 20
        
        """
        return int(apds_reading * 19 / self.APDS_MAX) + 1