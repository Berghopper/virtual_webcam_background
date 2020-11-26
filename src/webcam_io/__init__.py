import os

import cv2
import numpy as np
from pyfakewebcam import FakeWebcam

from src import Config


class Webcam:
    frame_buffer = []
    framerate = 0
    width = 0
    height = 0
    video_device_path = ""

    def __init__(self, width, height, framerate, video_device_path):
        self.width = width
        self.height = height
        self.framerate = framerate
        if os.path.exists(video_device_path):
            self.video_device_path = video_device_path
        else:
            raise TypeError(f"{video_device_path} Does not point to a valid webcam or video device.")


class WebcamInput(Webcam):
    def __init__(self, width, height, framerate, video_device_path, config):
        # load config specifics.
        super().__init__(width, height, framerate, video_device_path)
        self.config = config
        # initialize webcam
        self.webcam_videocapture = cv2.VideoCapture(self.video_device_path)

        # first set the appropriate codec, if one is specified.
        if self.config.get("mjpeg"):
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.webcam_videocapture.set(cv2.CAP_PROP_FOURCC, fourcc)

        # Configure the resolution and framerate of the real webcam
        if self.config.get("width"):
            self.webcam_videocapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get("width"))
        if self.config.get("height"):
            self.webcam_videocapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get("height"))
        if self.config.get("fps"):
            self.webcam_videocapture.set(cv2.CAP_PROP_FPS, self.config.get("fps"))

        # Run optimizations
        self.reduced_buffer = self.webcam_videocapture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Get the actual resolution (either webcam default or the configured one)
        self.width = int(self.webcam_videocapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.webcam_videocapture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # static image?
        self.supported_image_extensions = ("jpg", "jpeg", "png")
        self.is_static_image = any([self.video_device_path.lower().endswith(ext) for ext in self.supported_image_extensions])
        self.static_image = None
        if self.is_static_image:
            success, self.static_image = self.webcam_videocapture.read()
            # BGR to RGB
            self.static_image = self.static_image[..., ::-1]
            self.static_image = self.static_image.astype(np.float)

            if not success:
                raise ValueError(f"Static image {self.video_device_path} could not be loaded!")

    def get_frame(self):
        if self.is_static_image and self.static_image:
            return self.static_image
        success, frame = self.webcam_videocapture.read()
        if not success:
            raise ValueError("Webcam failed to read image!")
        frame = frame[..., ::-1]
        frame = frame.astype(np.float)
        return frame.astype(np.uint8)

    def close(self):
        self.webcam_videocapture.release()


class WebcamOutput(Webcam):
    NotImplemented

conf = Config(config_path="config.yaml")
webcam_inp = WebcamInput(640, 480, 30, '/dev/video0', conf)
webcam_out = FakeWebcam('/dev/video2', 640, 480)
while True:
    webcam_out.schedule_frame(webcam_inp.get_frame())