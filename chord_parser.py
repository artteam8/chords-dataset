import re
import json
from bs4 import BeautifulSoup
import requests
import os

from yandex_music import Album, Client, Playlist, Track




token = str(input())



client = Client(token).init()






def get_chords(song):
    lyrics_page=requests.get('https://chorder.ru' + song[2])
    lyrics_content = BeautifulSoup(lyrics_page.content, 'html.parser')
    lyrics = lyrics_content.find(id='song-text')
    
    return lyrics.get_text()


def get_all_chords():
    url = "https://chorder.ru/top100"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    
    items = soup.find_all(class_='item')


    songs=[]

    for item in items:
        
        title = item.find('div', class_='title')
        song_name = title.a.text if title else 'Неизвестно'
        song_link = title.a['href'] if title else 'Неизвестно'
        
        
        artist = item.find('div', class_='artist')
        artist_name = artist.text if artist else 'Неизвестно'
        
        
        songs.append([song_name, artist_name, song_link])
    all_songs = []
    for song in songs:
        chords = get_chords(song)
        new_song = song
        new_song.append(chords)
        all_songs.append(new_song)
    return all_songs


    






def download(track_id, token):
    
    os.system('cd ~/Documents/chords-dataset')
    os.system('source myenv/bin/activate')
    os.system(f'yandex-music-downloader --token "{token}" --quality 1 --add-lyrics --track-id "{track_id}"')





def get_song_id(song_name, client):
    result = client.search(text=song_name)
    song_object = result.tracks.results[0]
    song_id=song_object.id
    return song_id

def get_song_link(song_name, client):
    return f'https://music.yandex.ru/track/{get_song_id(song_name, client)}'










def data(token):



    for song in get_all_chords():

        song_text=song[3]



        s = song_text.split('\n')


        download(get_song_id(song[0], client), token)
        path = os.path.join(os.getcwd(), 'lyrics', f'{song[0].replace(' ', '_').lower()}.txt' )

        


        with open(path, 'r') as txt_file:
            timings = txt_file.read().split('\n')


        def chords():
            
            notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            chords = []

            for note in notes:
                chords.append(note)

            
            for note in notes:
                chords.append(note + "maj")

            
            for note in notes:
                chords.append(note + "min")

            
            for note in notes:
                chords.append(note + "7")
                chords.append(note + "maj7")
                chords.append(note + "m7")
                chords.append(note + "mMaj7")
                chords.append(note + "sus2")
                chords.append(note + "sus4")
                chords.append(note + "dim")
                chords.append(note + "aug")

            return chords

        chords=chords()


        

        print(chords)

        print(timings)

        t=[]
        for i in range(len(s)-1):
            if [chord for chord in chords if chord in s[i]]:

                
                
                string = s[i+1].replace('\r', '')
                t.append([s[i].replace('\r', '').strip(), string])
                
        print('////////////////////')
        print(t, '\n\n')



        """with open('chords.json', 'w') as f:
                                    json.dump(t, f)"""
        """
        with open('chords.json', 'r') as f:
            t=json.loads(f.read())
        """
        print('\n\n', t, '\n\n')


        time_steps=[]
        for i in range(len(timings)-1):
            time, string = timings[i].split(']')
            time=time.replace('[', '')

            time_end = timings[i+1].split()[0].replace('[', '').replace(']', '')


            time_steps.append([time + ' ' + time_end, string])

        print(time_steps, '\n\n')




        def chord_timings(chordstxt, timetxt):
            data=[]
            removed=0
            for i in range(len(chordstxt)):
                for j in range(len(timetxt)):
                    if  (chordstxt[i-removed][1] in timetxt[j-removed][1]):
                        data.append([timetxt[j-removed], chordstxt[i-removed]])
                        print('\n', timetxt[j-removed], '|', chordstxt[i-removed])
                        timetxt.pop(j-removed)
                        chordstxt.pop(i-removed)
                        removed+=1
            return data

        print('////////////////////\n\n\n\n')

        

        


        def replace_latin_with_cyrillic(text):
            
            replacements = {
                'b': 'б', 'k': 'к', 'm': 'м', 'h': 'н',  't': 'т ',
                'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с', 'y': 'у', 'x': 'х'
            }
            
            
            for latin, cyrillic in replacements.items():
                text = text.replace(latin, cyrillic)
            return text




        def preprocess(text):    
            return  replace_latin_with_cyrillic(  re.sub(r'[.,\-:"\'!()?—]', '', text.lower())   ).replace("  ", " ").replace('ё', 'е').strip()


        chords_preprocessed = [

            (tt[0], preprocess(tt[1])) for tt in t if tt[1].replace(' ', '')!=''

        ]

        timings_preprocessed = [

            (time[0], preprocess(time[1])) for time in time_steps if time[1].replace(' ', '')!=''

        ]






        

        for c in chords_preprocessed:
            print(c[0], c[1])
        print('\n\n\n')
        for i in timings_preprocessed:
            print(i[0], i[1])
        print('\n\n\n')













        result = []

        used_chords = set()



        result = []

        used_chords = set()

        for timing, timing_text in timings_preprocessed:
            matched_chords = []
            current_text = timing_text  

            for i, (chord, chord_text) in enumerate(chords_preprocessed):
                
                if i not in used_chords and chord_text in current_text:
                    matched_chords.append(chord)  
                    used_chords.add(i)  
                    current_text = current_text.replace(chord_text, '', 1).strip()  

            
            result.append((timing, matched_chords, timing_text))





        data = [ [t, [chord for cc in c for chord in cc.split()], l ]  for t, c, l in result]




        def split_chords_by_time(interval, chords):
            def time_to_seconds(time_str):
                """Преобразует время из формата мм:сс.сс в секунды."""
                minutes, seconds = map(float, time_str.split(':'))
                return minutes * 60 + seconds

            def seconds_to_time(seconds):
                """Преобразует секунды в формат мм:сс.сс."""
                minutes = int(seconds // 60)
                seconds = seconds % 60
                return f"{minutes:02}:{seconds:05.2f}"

            
            start_time, end_time = interval.split()
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)

            
            total_duration = end_seconds - start_seconds
            chord_duration = total_duration / len(chords)

            
            result = []
            for i, chord in enumerate(chords):
                chord_start = start_seconds + i * chord_duration
                chord_end = chord_start + chord_duration
                result.append((chord, seconds_to_time(chord_start), seconds_to_time(chord_end)))

            return result



        full_text_path = os.path.join(os.getcwd(), 'full_text', f'{song[0].replace(' ', '_').lower()}-text.json' )
        with open(full_text_path, 'w') as file:
            json.dump(data, file)


        every_chord = []

        for d in data:
            if len(d[1])>0:
                spl = split_chords_by_time(d[0], d[1])
                for sp in spl:
                    if sp[0] in chords:
                        every_chord.append(sp)




        for e in every_chord:
            print(e)

        save_chord_path = os.path.join(os.getcwd(), 'chords', f'{song[0].replace(' ', '_').lower()}.json' )
        with open(save_chord_path, 'w') as file:
            json.dump(every_chord, file)


data(token)