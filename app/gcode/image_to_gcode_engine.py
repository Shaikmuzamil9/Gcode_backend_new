import os
import uuid
import numpy as np
from scipy import ndimage
import imageio
from PIL import Image
from app.gcode.constants import circumferences

# ---------------- EDGE DETECTION ----------------

def sobel(image):
    image = np.array(image, dtype=float)
    image /= 255.0
    gx = ndimage.sobel(image, axis=0)
    gy = ndimage.sobel(image, axis=1)
    res = np.hypot(gx, gy)
    res /= np.max(res)
    res = np.array(res * 255, dtype=np.uint8)
    return res[2:-2, 2:-2, 0:3]


def convert_to_binary_edges(edges, threshold=32):
    result = np.maximum.reduce(
        [edges[:, :, 0], edges[:, :, 1], edges[:, :, 2]]
    ) >= threshold
    return result


# ---------------- GRAPH + GCODE ----------------

class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, x, y):
        self.nodes.append((x, y))

    def save_as_gcode(self, file):
        file.write("G21\n")  # mm
        file.write("G90\n")  # absolute positioning
        for x, y in self.nodes:
            file.write(f"G1 X{y} Y{-x}\n")


# ---------------- MAIN CONVERTER ----------------

def convert_image_to_gcode(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image not found")

    # Load image
    image = imageio.imread(image_path)

    # Sobel edge detection
    edges = sobel(image)
    edges = convert_to_binary_edges(edges)

    # Very simplified graph (practical + fast)
    graph = Graph()
    for x, y in np.argwhere(edges):
        graph.add_node(x, y)

    # Save gcode
    gcode_dir = os.path.join(
        os.path.dirname(image_path),
        "..",
        "gcodes"
    )
    gcode_dir = os.path.abspath(gcode_dir)
    os.makedirs(gcode_dir, exist_ok=True)

    gcode_filename = f"{uuid.uuid4()}.gcode"
    gcode_path = os.path.join(gcode_dir, gcode_filename)

    with open(gcode_path, "w") as f:
        graph.save_as_gcode(f)

    return gcode_path
