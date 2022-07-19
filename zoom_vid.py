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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import *
from kivy.uix.textinput import *
from kivy.uix.button import *
import time
import threading


# ******************CONFIG**************************************************

# **************************************************************************

class UIScreen(GridLayout):

    def __init__(self, **kwargs):
        super(UIScreen, self).__init__(**kwargs)
        self.status_string = "Click Process to Begin"
        self.rows = 4
        self.row_force_default = True
        self.row_default_height = 30
        self.column_default_height = 30
        self.add_widget(Label(text="ZoomIn Interval"))
        self.ZoomInInterval = TextInput(text=str(0), multiline=False, height=20)
        self.add_widget(self.ZoomInInterval)
        self.add_widget(Label(text="ZoomOut Interval"))
        self.ZoomOutInterval = TextInput(text=str(0), multiline=False)
        self.add_widget(self.ZoomOutInterval)
        self.add_widget(Label(text="File Location"))
        self.FileLocation = TextInput(text="Enter File Location Here", multiline=False)
        self.add_widget(self.FileLocation)
        self.button = Button(text='Process Videos', size_hint=(1, .2))
        self.add_widget(self.button)
        self.button.bind(on_press=self.button_clicked)
        self.StatusLabel = Label(text=self.status_string)
        self.add_widget(self.StatusLabel)
        self.process_active = False

    def update_button_thread(self):
        threading.Thread(target=self.update_button).start()

    def update_button(self):
        self.button.disabled = True
        self.button.text = "Please Wait"
        status_string = process_movie(self.FileLocation.text, int(self.ZoomInInterval.text),
                                      int(self.ZoomOutInterval.text))
        self.StatusLabel.text = status_string
        self.button.text = "Process Video"
        self.button.disabled = False

    def button_clicked(self, button):
        self.update_button_thread()


class AutoVidZoom(App):
    def __init__(self):
        super().__init__()

    def build(self):
        return UIScreen()


def grab_audio(video_location):

    try:
        movie_clip = VideoFileClip(video_location)

    except IOError:
        print("Invalid File Location or Type")
        return None

    except UnboundLocalError:
        print("Invalid File Location")
        return None

    return movie_clip.audio


def process_movie(video_location, zoom_in_interval, zoom_out_interval):
    movie = cv2.VideoCapture(video_location)
    fps = movie.get(cv2.cv2.CAP_PROP_FPS)
    width = int(movie.get(3))
    height = int(movie.get(4))
    audio = grab_audio(video_location)

    if audio is None:
        return "Audio Process Failure"

    frame_list = []
    video_time = 0
    zoom_time = 0

    if not movie.isOpened():
        return "Video Stream Error"

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
        return "Success"

    else:
        return "No Frames to Process..."


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    AutoVidZoom().run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
