# See config section to setup script for your videos

import os
try:
    from moviepy.editor import *

except:
    os.system("pip install moviepy")

try:
    import cv2

except:
    os.system("pip install opencv-python")

try:
    import kivy
except:
    os.system("pip install kivy")

from kivy.app import App
from kivy.uix.boxlayout import *
from kivy.uix.label import *
from kivy.uix.textinput import *
from kivy.uix.button import *


# ******************CONFIG**************************************************
# video_location = "/home/*****/Videos/"  # Location of Video Folder
# video = "sample-mp4-file.mp4" # filename
zoom_in_interval = 4    # Change Zoom In Time Interval
zoom_out_interval = 10  # Change Zoom Out Time Interval
# **************************************************************************


class AutoVidZoom(App):
    def __init__(self):
        super().__init__()
        self.text_input = None
        self.label = None
        self.process_active = False

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        self.label = Label(text='Status: Enter Location: ')
        self.text_input = TextInput(font_size=20, multiline=False, height=5, size_hint=(1,.2))
        button = Button(text='Process Videos', size_hint=(1, .2))
        button.bind(on_press=self.button_clicked)

        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        return layout

    def button_clicked(self, button):
        self.label.text = "Status: Processing Video Please Wait..."
        video_location = self.text_input.text

        if not self.process_active:
            self.process_active = True
            process_movie(video_location)
            self.process_active = False
            self.label.text = "Status: Processing Complete. Enter new Location"


def grab_audio(video_location):

    try:
        movie_clip = VideoFileClip(video_location)

    except IOError:
        print("Invalid File Location or Type")

    except UnboundLocalError:
        print("Invalid File Location")

    return movie_clip.audio


def process_movie(video_location):
    movie = cv2.VideoCapture(video_location)
    fps = movie.get(cv2.cv2.CAP_PROP_FPS)
    width = int(movie.get(3))
    height = int(movie.get(4))
    audio = grab_audio(video_location)
    frame_list = []
    video_time = 0
    zoom_time = 0

    if not movie.isOpened():
        print("Video Stream Error")

    while movie.isOpened():
        ret, frame = movie.read()
        video_time = video_time + 1

        if ret:
            if video_time / fps >= zoom_out_interval:

                zoom_time = zoom_time + 1
                # Enlarge Image
                frame = cv2.resize(frame, (width * 2, height * 2),  interpolation=cv2.INTER_NEAREST)

                # Crop to size
                frame = frame[0:height, 0:width]

                if zoom_time / fps >= zoom_in_interval:
                    zoom_time = 0
                    video_time = 0

            frame_list.append(ImageClip(frame).set_duration(1 / fps))

        else:
            break

    if frame_list:
        new_video = concatenate_videoclips(frame_list, method="compose")
        final_video = new_video.set_audio(audio)
        final_video.write_videofile("test.mp4", fps=fps)
        movie.release()
        cv2.destroyAllWindows()

    else:
        print("No Frames to Process...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    AutoVidZoom().run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
