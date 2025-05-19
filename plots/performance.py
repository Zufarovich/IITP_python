from pathlib import Path
from timeit import timeit
from tqdm import tqdm

import cv2
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from interpolation.image_process import process_interpolation


def performance_scale_factor(path: Path, out_path: Path, interpolation_methods: dict):
    sns.set_style("darkgrid")
    
    scale_factor_list = np.linspace(2, 8, 4, dtype=int)
    times = np.empty_like(scale_factor_list)

    for method_name, method in interpolation_methods.items():
        times = []
        img = cv2.imread(path)
        width = img.shape[1]
        height = img.shape[0]
        
        print(f">>> Method:{method_name}\n")
        for scale in tqdm(scale_factor_list):
            time = timeit(
                f"""{method_name}(
                    path, out_path, width, height),""",
                globals={f"{method_name}": method, "path":path, "out_path": out_path,
                         "width": int(width*scale), "height": int(height*scale)},
                number = 10,
            )
            times.append(time)
            
        plt.plot(scale_factor_list, times, "o-", label=f"{method_name} method")
    
    plt.xlabel("Scale factor")
    plt.ylabel("Time, s")
    plt.title("Performance of `image interpolation`")
    plt.grid(visible=True)
    plt.legend()
    plt.show()
    

if __name__ == "__main__":
    file_path = Path("lantern.jpeg")
    output_path = Path("lantern1.jpeg")
    
    interpolation_methods = {
        "process_interpolation": process_interpolation
    }

    print(">>> Testing performance...\n")

    performance_scale_factor(file_path, output_path, interpolation_methods)