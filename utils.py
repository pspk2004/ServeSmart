import qrcode
import io
import base64

def generate_qr_code(token_data):
    """
    Generates a QR code from the given data and returns it as a base64 encoded string.
    """
    qr_img = qrcode.make(token_data)
    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str