from fastapi import FastAPI, Body, File
import uvicorn
from pydantic import BaseModel
import cv2
import numpy as np
from typing import Union
import os

from config import model_path, image_size
from model import Model


class PredictResponseProbsSchema(BaseModel):
    cat: float
    dog: float


class PredictResponseClassnameSchema(BaseModel):
    classname: str


model = Model(
    model_path=model_path,
    image_size=image_size,
)

service_name = os.environ.get('SERVICE_NAME', 'Cat-Dog classification service')


app = FastAPI(title=service_name)


@app.post('/predict', response_model=Union[PredictResponseProbsSchema, PredictResponseClassnameSchema])
async def predict(image: bytes = File(...), classname_only: bool = Body(...)):
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    preds = model.predict(image)
    if classname_only:
        return PredictResponseClassnameSchema(classname=max(preds, key=lambda key: preds[key]))
    return PredictResponseProbsSchema(**preds)


if __name__ == '__main__':
    uvicorn.run('service:app', host='0.0.0.0')
