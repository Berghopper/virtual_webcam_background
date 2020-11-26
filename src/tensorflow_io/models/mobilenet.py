import numpy as np
from src.tensorflow_io.models.abstract_model import AbstractModel


class Mobilenet(AbstractModel):
    def __init__(self, model_path):
        AbstractModel.__init__(self, model_path, 1, 2, 4)

    def preprocessing(self, frame):
        return np.subtract(np.divide(frame, 127.5), 1.0)


