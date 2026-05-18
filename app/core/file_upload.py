from pathlib import Path
from uuid import uuid4
import base64

from fastapi import UploadFile


UPLOAD_ROOT = Path("uploads")


def build_upload_path(*parts: str) -> Path:
    path = UPLOAD_ROOT.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    target_dir = build_upload_path(folder)
    suffix = Path(upload_file.filename or "").suffix
    filename = f"{uuid4().hex}{suffix}"
    target_file = target_dir / filename

    content = await upload_file.read()
    target_file.write_bytes(content)

    return str(target_file).replace("\\", "/")


def save_base64_file(data: str, folder: str) -> str:
    target_dir = build_upload_path(folder)

    content_type = "application/octet-stream"
    encoded = data

    if data.startswith("data:") and ";base64," in data:
        header, encoded = data.split(";base64,", 1)
        content_type = header[5:].split(";")[0]

    extension_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    suffix = extension_map.get(content_type, ".bin")
    filename = f"{uuid4().hex}{suffix}"
    target_file = target_dir / filename
    target_file.write_bytes(base64.b64decode(encoded))
    return str(target_file).replace("\\", "/")
