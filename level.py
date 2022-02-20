import pyray as rl

class Level:
    def __init__(self):
        print("Loading level")
        self._music = rl.load_music_stream('music/One-Bard-Band.mp3')
        rl.play_music_stream(self._music)

    def __del__(self):
        print("Unloading level")
        rl.stop_music_stream(self._music)

    def update_music_stream(self):
        rl.update_music_stream(self._music)