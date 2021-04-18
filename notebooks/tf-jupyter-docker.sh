docker run -p 8888:8888 --gpus all -it -v /mnt/HDD/datasets:/mnt/HDD/datasets -v $PWD/..:/tf -w /tf --rm tensorflow/tensorflow:latest-gpu-jupyter
