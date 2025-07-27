import sys, os, time
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl, QTimer

from ui import Ui_MainWindow


class MP3Player(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.current_songs = []
        self.volume = 50
        self.volume_is_hide = True

        self.timer = QTimer(self)
        self.timer.start(100)
        self.timer.timeout.connect(self.move_music_slider)

        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.handle_end_of_media)
        self.player.setVolume(self.volume)

        self.addButton.clicked.connect(self.add)
        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause) 
        self.rightButton.clicked.connect(self.next_music)
        self.leftButton.clicked.connect(self.prev_music)
        self.settingsButton.clicked.connect(self.setting_hide)
        self.musicSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.musicSlider.value()))
        self.volumeSlider.valueChanged.connect(self.volume_changed) 
        

    def play(self):
        try:
            current_selection = self.musicList.currentRow()
            current_song = self.current_songs[current_selection]
    
            track = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(track)
            self.player.play()
            self.move_music_slider()
        except Exception as e:
            print(e)    

    def pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play() 

    def next_music(self):
        try:
            next_selection = self.musicList.currentRow() + 1
            if next_selection == len(self.current_songs):
                next_selection = 0

            next_music = self.current_songs[next_selection]
            self.musicList.setCurrentRow(next_selection)
        
            track = QMediaContent(QUrl.fromLocalFile(next_music))
            self.player.setMedia(track)
            self.player.play()
            self.move_music_slider()

        except Exception:
            pass    

    def prev_music(self):
        try:
            prev_selection = self.musicList.currentRow() - 1
            if prev_selection == -1:
                prev_selection = len(self.current_songs) - 1

            prev_music = self.current_songs[prev_selection]
            self.musicList.setCurrentRow(prev_selection)
        
            track = QMediaContent(QUrl.fromLocalFile(prev_music))
            self.player.setMedia(track)
            self.player.play()
            self.move_music_slider()  

        except Exception:
            pass      

    def add(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(self,
                caption='Add songs', directory=r':\\',
                filter="Supported Files (*.mp3;*.mpeg;*.ogg;*.MP3)")
            if files:
                for file in files:
                    self.current_songs.append(file)
                    self.musicList.addItem(os.path.basename(file))
        except:
            pass        

    def move_music_slider(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.musicSlider.setMinimum(0)
            self.musicSlider.setMaximum(self.player.duration())
            slider_pos = self.player.position()
            self.musicSlider.setValue(slider_pos)

            cur_time = time.strftime('%H:%M:%S', time.gmtime(slider_pos // 1000))
            music_duration = time.strftime('%H:%M:%S', time.gmtime(self.player.duration() // 1000))
            self.curTime.setText(f"{cur_time}")
            self.musicDuration.setText(f"{music_duration}")
    
    def volume_changed(self):
        try:
            self.volume = self.volumeSlider.value()
            self.player.setVolume(self.volume)
            self.volumeValue.setText(f"{self.volume}%")
        except Exception:
            pass 

    def setting_hide(self):
        self.volumeSlider.setVisible(not self.volume_is_hide) 
        self.volumeValue.setVisible(not self.volume_is_hide)
        self.volume_is_hide = not self.volume_is_hide

    def handle_end_of_media(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.musicSlider.setValue(self.player.duration())   
            self.curTime.setText(f"{time.strftime('%H:%M:%S', time.gmtime(self.player.duration() // 1000))}") 
 


def main():
    app = QApplication(sys.argv)
    player = MP3Player()
    player.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()   