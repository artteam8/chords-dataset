def chords():
    # Мажорные, минорные и дополнительные аккорды
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chords = []

    # Мажорные аккорды
    for note in notes:
        chords.append(note + "maj")

    # Минорные аккорды
    for note in notes:
        chords.append(note + "min")

    # Дополнительные аккорды
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

s = song.split('\n'):
chords=chords()


timings = ?



t=[]
for i in range(len(s)):
    if [chord in chords if chord in s[i]]:
        #chords_in_string = s[i].split()
        #строка аккордов
        string = s[i+1]
        t.append(s[i], string)
        #timing = timings[string]
for tt in t:
    print(tt)

    



"""
[[куплет|B:DUX-UDUX]]
  F#m
 Тёплое место, но улицы ждут
      C#m          F#m
 Отпечатков наших ног.
              E
 Звёздная пыль на сапогах.
  F#m
 Мягкое кресло, клетчатый плед,
       C#m             F#m
 Не нажатый вовремя курок.
                       E
 Солнечный день в ослепительных снах.

[[припев]]
            F#m
   Группа крови - на рукаве,
                   C#m
   Мой порядковый номер - на рукаве.
        Bm7
   Пожелай мне удачи в бою,
        E
   Пожелай мне
         F#m
   Не остаться в этой траве,
         C#m
   Не остаться в этой траве.
        Bm7
   Пожелай мне удачи,
        E        F#m
   Пожелай мне удачи.

{{проигрыш}}
 | F#m C#m7 |

[[куплет_2]]
   F#m
 И есть чем платить, но я не хочу
    C#m          F#m
 Победы любой ценой.
                E
 Я никому не хочу ставить ногу на грудь.
      F#m
 Я хотел бы остаться с тобой,
   C#m                F#m
 Просто остаться с тобой,
                             E
 Но высокая в небе звезда зовёт меня в путь.

[[припев]]

{{проигрыш_2}}
 | F#m C#m |
"""