import numpy as np
from typing import Tuple
import cv2
import onnxruntime as ort


class Model:
    def __init__(self, model_path: str, image_size: Tuple[int, int]):
        self._ort_session = ort.InferenceSession(
            model_path,
            providers=[
                'CUDAExecutionProvider',
                'CPUExecutionProvider',
            ],
        )
        self._model_input_name = [inp.name for inp in self._ort_session.get_inputs()][0]
        self._image_size = image_size

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32)
        image = cv2.resize(image, self._image_size) / np.iinfo(np.uint8).max
        image = np.transpose(image, (2, 0, 1))
        image -= np.array([0.485, 0.456, 0.406])[:, None, None]
        image /= np.array([0.229, 0.224, 0.225])[:, None, None]
        return image

    def predict(self, image: np.ndarray) -> dict[str, float]:
        image = self._preprocess(image)
        logits = self._ort_session.run(None, {self._model_input_name: image[None]})[0][0]
        probs = 1 / (1 + np.exp(-logits))
        return {
            'cat': probs[0],
            'dog': probs[1],
        }
