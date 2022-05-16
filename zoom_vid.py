# See config section to setup script for your videos

try:
    from moviepy.editor import *

except:
    print("pip install moviepy")

try:
    import cv2

except:
    print("pip install opencv-python")


# ******************CONFIG**************************************************
video_location = "/home/*****/Videos/"  # Location of Video Folder
video = "sample-mp4-file.mp4" # filename
zoom_in_interval = 4    # Change Zoom In Time Interval
zoom_out_interval = 10  # Change Zoom Out Time Interval
# **************************************************************************


def grab_audio():
    movie_clip = VideoFileClip(video_location + video)
    return movie_clip.audio


def process_movie():
    movie = cv2.VideoCapture(video_location + video)
    fps = movie.get(cv2.cv2.CAP_PROP_FPS)
    width = int(movie.get(3))
    height = int(movie.get(4))
    audio = grab_audio()
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
    process_movie()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
