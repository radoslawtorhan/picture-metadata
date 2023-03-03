from datetime import datetime
from pathlib import Path
import sys
from typing import Optional

import exif

root = Path(__file__).parent


class ImageMetaData:
    def __init__(self):
        self.device: str = ""
        self.width_px: int = 0
        self.height_px: int = 0
        self.datetime: Optional[datetime] = None


def get_metadata_from_file(path: Path) -> ImageMetaData:
    if not path.exists():
        raise Exception("File doesn't exist!")
    with open(path, "rb") as image_file:
        try:
            image = exif.Image(image_file)
        except Exception as e:
            raise Exception("Can't open the file") from e
    if not image.has_exif:
        raise Exception("This image doesn't have the metadata at all!")
    keys = image.list_all()
    raw_data = {}
    for key in keys:
        try:
            value = getattr(image, key)
        except:
            continue
        raw_data[key] = value
    data = ImageMetaData()
    data.device = f"{raw_data.get('make')} {raw_data.get('model')}"
    data.width_px = int(raw_data.get("pixel_x_dimension", 0))
    data.height_px = int(raw_data.get("pixel_y_dimension", 0))

    try:
        data.datetime = datetime.strptime(
            raw_data.get("datetime", ""), "%Y:%m:%d %H:%M:%S"
        )
    except:
        print("unknown datetime format!")
        data.datetime = None
    return data


if __name__ == "__main__":
    file_name = "my-file.jpg"
    path = root / file_name
    try:
        data = get_metadata_from_file(path)
    except Exception as e:
        print("Can't read metadata from file:", e)
        sys.exit(0)
    print("device:", data.device)
    print("width:", data.width_px)
    print("height:", data.height_px)
    print("datetime:", data.datetime)