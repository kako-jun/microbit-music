from microbit import *
import music

# 曲データ辞書
songs = {
    "DQ序曲": [
        'G4:2', 'C5:2', 'E5:2', 'G5:2', 'C6:4',
        'C4:4', 'D4:4', 'E4:4', 'F4:4', 'G4:4', 'A4:4', 'B4:4', 'C5:4',
        'G4:4', 'E4:4', 'C4:4'
    ],
    "FF序曲": [
        'C4:2', 'E4:2', 'G4:2', 'C5:2', 'E5:2', 'G5:2', 'C6:2',
        'E5:2', 'G5:2', 'C5:2', 'G4:2', 'E4:2', 'C4:2'
    ]
}

# グローバル変数
song_names = list(songs.keys())
current_song_index = 0
shift = 0
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def shift_note(note, shift):
    """音階をシフトする関数"""
    pitch = note[:-1]
    octave = int(note[-1])
    idx = notes.index(pitch) + shift

    # オクターブ調整
    while idx < 0:
        idx += 12
        octave -= 1
    while idx >= 12:
        idx -= 12
        octave += 1

    return notes[idx] + str(octave)


def display_pitch(note):
    """音の高さをLEDバー表示"""
    pitch = note[:-1]
    idx = notes.index(pitch)
    col = idx // 3  # 12音階を5列に分割
    level = (idx % 3) + 1  # 簡易高さ（1～3）

    img = Image('00000:'*5)
    for row in range(5 - level, 5):  # 下から点灯
        img.set_pixel(col, row, 9)
    display.show(img)


def next_song():
    """次の曲へ"""
    global current_song_index, shift
    current_song_index = (current_song_index + 1) % len(song_names)
    shift = 0
    display.scroll(song_names[current_song_index])


def prev_song():
    """前の曲へ"""
    global current_song_index, shift
    current_song_index = (current_song_index - 1) % len(song_names)
    shift = 0
    display.scroll(song_names[current_song_index])


# メインループ
display.scroll("Ready")

while True:
    # ボタン入力チェック
    if button_a.is_pressed() and button_b.is_pressed():
        # 同時押し：キーリセット
        shift = 0
        display.scroll("Key Reset")
    elif button_a.is_pressed():
        sleep(800)
        if button_a.is_pressed():
            # A長押し：前の曲
            prev_song()
        else:
            # A短押し：半音下げ
            shift -= 1
            display.scroll("Key: " + str(shift))
    elif button_b.is_pressed():
        sleep(800)
        if button_b.is_pressed():
            # B長押し：次の曲
            next_song()
        else:
            # B短押し：半音上げ
            shift += 1
            display.scroll("Key: " + str(shift))

    # 曲を演奏
    for n in songs[song_names[current_song_index]]:
        base_note = n.split(':')[0]
        length = n.split(':')[1]
        new_note = shift_note(base_note, shift) + ':' + length

        # LED表示
        display_pitch(base_note)

        # 音を再生
        music.play(new_note, wait=True)

        # ボタンチェック（曲の途中でも切り替え可能）
        if button_a.is_pressed() or button_b.is_pressed():
            break

    sleep(500)  # 曲間の待機時間
