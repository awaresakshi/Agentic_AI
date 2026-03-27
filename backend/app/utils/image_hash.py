import hashlib

def generate_image_hash(file_path):

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    return hashlib.md5(file_bytes).hexdigest()