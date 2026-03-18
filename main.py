from microbit import *
import music

# 曲データ辞書
# DQ序曲: ドラゴンクエスト序曲マーチ冒頭（Bb major → C major に移調）
# FF序曲: ファイナルファンタジー プレリュード（C major アルペジオ）
songs = {
    "DQ序曲": [
        # 序曲マーチ: ファンファーレ冒頭
        'C5:1', 'C5:1', 'C5:1', 'C5:4',
        'C5:1', 'D5:1', 'E5:1', 'F5:1', 'G5:4',
        'G5:1', 'F5:1', 'E5:1', 'F5:1', 'E5:1', 'D5:1',
        'C5:2', 'D5:2', 'E5:4',
        # マーチ主題
        'E5:1', 'E5:1', 'E5:1', 'E5:4',
        'E5:1', 'F5:1', 'G5:1', 'A5:1', 'B5:4',
        'B5:1', 'A5:1', 'G5:1', 'A5:1', 'G5:1', 'F5:1',
        'E5:2', 'F5:2', 'G5:4',
    ],
    "FF序曲": [
        # プレリュード: 上昇アルペジオ
        'C4:1', 'D4:1', 'E4:1', 'G4:1',
        'C5:1', 'D5:1', 'E5:1', 'G5:1',
        'C6:1', 'G5:1', 'E5:1', 'D5:1',
        'C5:1', 'G4:1', 'E4:1', 'D4:1',
        # 2巡目（半音上がったパターン）
        'E4:1', 'G4:1', 'A4:1', 'C5:1',
        'E5:1', 'G5:1', 'A5:1', 'C6:1',
        'A5:1', 'G5:1', 'E5:1', 'C5:1',
        'A4:1', 'G4:1', 'E4:1', 'C4:1',
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
    """音の高さをLEDバー表示（5列すべてを使用）"""
    pitch = note[:-1]
    idx = notes.index(pitch)
    col = idx * 5 // 12  # 12音階を5列に均等分配（0-4）
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
display.scroll(song_names[current_song_index])

while True:
    # ボタン入力チェック
    if button_a.is_pressed() and button_b.is_pressed():
        # 同時押し：キーリセット
        shift = 0
        display.scroll("Key Reset")
    elif button_a.is_pressed():
        # 非ブロッキング長押し判定（50ms×16回 = 800ms）
        held = True
        for _ in range(16):
            sleep(50)
            if not button_a.is_pressed():
                held = False
                break
        if held:
            # A長押し：前の曲
            prev_song()
        else:
            # A短押し：半音下げ（下限-12）
            if shift > -12:
                shift -= 1
            display.scroll("Key: " + str(shift))
    elif button_b.is_pressed():
        # 非ブロッキング長押し判定（50ms×16回 = 800ms）
        held = True
        for _ in range(16):
            sleep(50)
            if not button_b.is_pressed():
                held = False
                break
        if held:
            # B長押し：次の曲
            next_song()
        else:
            # B短押し：半音上げ（上限+12）
            if shift < 12:
                shift += 1
            display.scroll("Key: " + str(shift))

    # 曲を演奏
    for n in songs[song_names[current_song_index]]:
        base_note = n.split(':')[0]
        length = n.split(':')[1]
        shifted = shift_note(base_note, shift)
        new_note = shifted + ':' + length

        # LED表示（キー変更後の音を表示）
        display_pitch(shifted)

        # 音を再生
        music.play(new_note, wait=True)

        # ボタンチェック（曲の途中でも切り替え可能）
        if button_a.is_pressed() or button_b.is_pressed():
            break

    sleep(500)  # 曲間の待機時間
