import os
import json
import music21 as m21

KERN_DATASET_PATH = "Data preprocessing/deutschl/test"
SAVE_DIR = "Data preprocessing/dataset"
SINGLE_FILE_DATA_SET = "file_dataset"
MAPPING_PATH = "mapping.json"
SEQUENCE_LENGTH = 64
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

def load(file_path):
    with open(file_path,'r') as fp:
        song = fp.read()
    return song

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
        
def create_single_file_dataset (dataset_path, file_dataset_path, sequence_length):
    new_song_delimiter = "/ " * sequence_length
    songs = ""
    #load encoded songs and add delimiters
    for path, _,files in os.walk (dataset_path):
        for file in files:
            file_path = os. path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + new_song_delimiter
    
    songs = songs[:-1]

    with open(file_dataset_path, "w") as fp:
        fp.write(songs)
        return songs
    
def create_mapping (songs, mapping_path):
    mappings = {}
    
    #identify the vocabulary
    songs = songs.split()
    vocabulary = list (set (songs))
    
    # create mappings
    for i, symbol in enumerate (vocabulary):
        mappings [symbol] = i
    
    #save voabulary to a json file
    with open (mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)

def main():
    preprocess (KERN_DATASET_PATH)
    songs = create_single_file_dataset (SAVE_DIR, SINGLE_FILE_DATA_SET, SEQUENCE_LENGTH)
    create_mapping (songs, MAPPING_PATH)

if __name__ == "__main__":
    main ()
