FROM python:3.10-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir onnxruntime==1.17.1

WORKDIR /build
COPY dependencies/service.requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /model
COPY model/model.onnx model.onnx

WORKDIR /service
COPY service/*.py .

CMD ["python", "service.py"]
