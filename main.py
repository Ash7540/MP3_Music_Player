import os
import random
import time

from packages import *

class MyApp(MDApp):
    def build(self):

        layout = MDRelativeLayout(md_bg_color=[0, 0, 0, 85])

        self.music_dir = "E:/my_projects/mp_player"

        self.music_file = os.listdir(self.music_dir)
        # print(self.music_file)

        self.song_list = [x for x in self.music_file if x.endswith(('mp3'))]
        self.song_count = len(self.song_list)
        # print(self.song_list)

        self.label = Label(pos_hint={'center_x': 0.5, 'center_y': 0.96}, size_hint=(1, 1), font_size=20)

        self.image = Image(pos_hint={'center_x': 0.5, 'center_y': 0.55}, size_hint=(0.8, 0.75))

        self.currentTime = Label(text="00:00", pos_hint={'center_x': 0.16, 'center_y': 0.145}, size_hint=(1, 1), font_size=18)

        self.totalTime = Label(text="00:00", pos_hint={'center_x': 0.84, 'center_y': 0.145}, size_hint=(1, 1), font_size=18)

        self.progressbar = ProgressBar(max=100, value=0, pos_hint={'center_x': 0.5, 'center_y': 0.12}, size_hint=(0.8, 0.75))

        self.volumeslider = Slider(min=0, max=1, value=0.5, orientation='horizontal', pos_hint={'center_x': 0.2, 'center_y': 0.05}, size_hint=(0.2, 0.2))

        # self.switch =Switch(pos_hint={'center_x': 0.65, 'center_y': 0.05})

        self.playbutton = MDIconButton(pos_hint={'center_x': 0.4, 'center_y': 0.05}, icon='play.png', on_press=self.play)
        self.stopbutton = MDIconButton(pos_hint={'center_x': 0.5, 'center_y': 0.05}, icon='stop.png', on_press=self.stop, disabled=True)
        # self.previousbutton = MDIconButton(pos_hint={'center_x': 0.6, 'center_y': 0.05}, icon='previous.png', on_press=self.stop)
        # self.nextbutton = MDIconButton(pos_hint={'center_x': 0.68, 'center_y': 0.05}, icon='next.png', on_press=self.stop)

        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        # layout.add_widget(self.previousbutton)
        # layout.add_widget(self.nextbutton)
        layout.add_widget(self.label)
        layout.add_widget(self.image)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.currentTime)
        layout.add_widget(self.totalTime)
        layout.add_widget(self.volumeslider)
        # layout.add_widget(self.switch)


        Clock.schedule_once(self.play)

        def volume(instance, value):
            self.sound.volume = value

        self.volumeslider.bind(value=volume)

        # def mute(instance, value):
        #     if value==True:
        #         self.sound.volume = 0
        #     else:
        #         self.sound.volume = 1
        # self.switch.bind(active=mute)

        return layout

    def play(self, obj):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.song_list[random.randrange(0, self.song_count)]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.song_title))

        self.label.text = "*** Playing ~ "+self.song_title[2:-4]+" ***"
        self.image.source = self.song_title[0]+".jpeg"

        self.sound.play()

        self.progressbarEvent = Clock.schedule_interval(self.update_progress, self.sound.length/60)
        self.setTimeEvent = Clock.schedule_interval(self.setTime, 1)

    def stop(self, obj):
        self.playbutton.disabled = False
        self.stopbutton.disabled = True
        self.sound.stop()

        self.progressbarEvent.cancel()
        self.setTimeEvent.cancel()
        self.progressbar.value = 0
        self.currentTime.text = "00:00"
        self.totalTime.text = "00:00"

    def update_progress(self, value):
        if self.progressbar.value < 100:
            self.progressbar.value += 1

    def setTime(self, t):
        current_Time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
        total_Time = time.strftime('%M:%S', time.gmtime(self.sound.length))

        self.currentTime.text = current_Time
        self.totalTime.text = total_Time

if __name__ == '__main__':
    MyApp().run()
