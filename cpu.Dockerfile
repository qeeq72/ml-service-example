FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    python3-pip \
    make \
    wget \
    ffmpeg \
    libsm6 \
    libxext6

RUN pip install --no-cache-dir onnxruntime==1.17.1

WORKDIR /build
COPY dependencies/service.requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /model
COPY model/model.onnx model.onnx

WORKDIR /service
COPY service/*.py .

CMD ["python3", "service.py"]
