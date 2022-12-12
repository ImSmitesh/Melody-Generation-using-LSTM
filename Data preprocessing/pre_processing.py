import os
import music21 as m21

KERN_DATASET_PATH = "Data preprocessing/deutschl/test"
SAVE_DIR = "Data preprocessing/dataset"
ACCEPTABLE_DURATIONS = [
    0.25,
    0.5,
    0.75,
    1.0,
    1.5,
    2,
    3
]

def load_songs_in_kern(dataset_path):
    songs = []
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:
            if file [-3:] == "krn":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
    return songs

def has_acceptable_durations(song, acceptable_duration):
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_duration:
            return False
    return True

def transpose(song):
    parts = song.getElementsByClass (m21.stream.Part)
    measures_part0 = parts[0].getElementsByClass (m21.stream.Measure)
    key = measures_part0 [0][4]

    if not isinstance(key, m21.key.Key):
        key = song. analyze ("key")
    
    if key.mode == 'major':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == 'minor':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))
    
    transposed_song = song.transpose(interval)

    return transposed_song

def encode_song (song, time_step = 0.25):
    encoded_song = []
    for event in song.flat.notesAndRests:
        #handle notes
        if isinstance (event, m21.note.Note):
            symbol = event.pitch.midi # 60
        # handle rests
        elif isinstance (event, m21.note.Rest):
            symbol = ""
        
        #convert the note/rest into time series notation
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):
            if step== 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")
            
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song

def preprocess(dataset_path):

    print('Loading Songs........')
    songs = load_songs_in_kern(dataset_path)
    print(f'loaded {len(songs)} songs.')

    for i, song in enumerate(songs):

        # Filter not acceptable duration songs
        if not has_acceptable_durations(song, ACCEPTABLE_DURATIONS):
            continue

        # Transpose songs to Cmajor/Aminor
        song = transpose(song)

        # Encode songs with music time series representation 
        encoded_song = encode_song(song)

        # Save files
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path,'w') as fp:
            fp.write(encoded_song)

if __name__ == "__main__":
    songs = load_songs_in_kern(KERN_DATASET_PATH)
    print(f'loaded {len(songs)} songs.')
    song = songs[0]
    preprocess(KERN_DATASET_PATH)
    # trans = transpose(song)
    # trans.show()