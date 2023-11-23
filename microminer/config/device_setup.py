import torch

# Check if CUDA (GPU) is available and if so, set the device to GPU
def set_device():
    if torch.cuda.is_available():  
        dev = "cuda:0" 
    else:  
        dev = "cpu"  

    device = torch.device(dev)

    return device