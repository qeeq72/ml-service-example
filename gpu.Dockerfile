FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

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

RUN pip install --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/ --no-cache-dir onnxruntime-gpu==1.17.1

WORKDIR /build
COPY dependencies/service.requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /model
COPY model/model.onnx model.onnx

WORKDIR /service
COPY service/*.py .

CMD ["python3", "service.py"]
