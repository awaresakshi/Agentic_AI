def allowed_file(filename):
    """
    Check if the uploaded file is allowed based on extension
    """
    allowed_extensions = {"png", "jpg", "jpeg", "pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions