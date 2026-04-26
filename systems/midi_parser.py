import mido, math, os

class LevelLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.notes=[]

    def parse(self):
        if not os.path.exists(self.filepath):
            print(f"Warning: {self.filepath} does not exist, Generating Dummy Sequence.")
            return self._generate_dummy_level()

        mid  = mido.MidiFile(self.filepath)
        ticks_per_beat = mid.ticks_per_beat

        absolute_time = 0.0
        current_tempo = 500000
        for msg in mido.merge_tracks(mid.tracks):
            delta_ticks = msg.time
            delta_seconds = (delta_ticks/ticks_per_beat)*(current_tempo/1_000_000.0)
            absolute_time += delta_seconds

            if msg.type == 'set_tempo': current_tempo = msg.tempo
            elif msg.type == 'note_on' and msg.velocity > 0:
                angle = (msg.note%24)*(math.pi/12)
                radius = 5+(msg.velocity/127.0)*10
                self.notes.append({
                    'hit_time': absolute_time,
                    'angle': angle,
                    'radius': radius,
                    'pitch': msg.note
                })
        return self.notes

    def _generate_dummy_level(self):
        notes = []
        for i in range(40):
            hit_time = 2.0 + i *0.5
            angle = (i%8)*(math.pi/4)
            notes.append({
                'hit_time': hit_time,
                'angle': angle,
                'radius': 10 + (i%3)*2,
                'pitch': 60
            })
        return notes


