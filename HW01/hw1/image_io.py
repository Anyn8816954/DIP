import cv2
import numpy as np


def read_image(path, flags=cv2.IMREAD_COLOR):
    # imread has trouble with Chinese paths on some Windows installations.
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, flags)
    if image is None:
        raise ValueError(f'Cannot decode image: {path}')
    return image


def write_image(path, image):
    success, data = cv2.imencode(path.suffix, image)
    if not success:
        raise ValueError(f'Cannot encode image: {path}')
    data.tofile(str(path))
