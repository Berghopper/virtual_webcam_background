import numpy as np
from src.tensorflow_io.models.abstract_model import AbstractModel


class Resnet50(AbstractModel):
    def __init__(self, model_path):
        AbstractModel.__init__(self, model_path, 6, 5, 2)

    def preprocessing(self, frame):
        return np.add(frame, np.array([-123.15, -115.90, -103.06]))


