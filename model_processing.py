import torch
from torchvision import models
from torchvision import transforms as T
import cv2
import numpy as np
from PIL import Image
import io

model = models.segmentation.deeplabv3_resnet101(weights='DeepLabV3_ResNet101_Weights.DEFAULT', progress=True)

device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)
model.eval()


PERSON_CLASS_ID = 15

preprocess = T.Compose([
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

print(f"Model loaded and running on device {device}")

def process_image(image_bytes:bytes, effect:str):
    original_image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    original_image = np.array(original_image_pil)

    input_tensor = preprocess(original_image_pil).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)['out'][0]

    output_predictions = output.argmax(0)
    prediction_mask = (output_predictions == PERSON_CLASS_ID).cpu().numpy().astype(np.uint8)


    pred_mask_resized = cv2.resize(prediction_mask, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)

    if effect == "remove_bg":
        original_rgba = original_image_pil.convert("RGBA")
        mask_pil = Image.fromarray((pred_mask_resized * 255).astype('uint8'), mode='L')
        transparent_background = Image.new('RGBA', original_rgba.size, (0, 0, 0, 0))
        transparent_background.paste(original_rgba, (0, 0), mask_pil)
        byte_buffer = io.BytesIO()
        transparent_background.save(byte_buffer, format="PNG")
        byte_buffer.seek(0) # Go to the beginning of the buffer
        return byte_buffer
    
    elif effect == "bokeh":
        blurred_bg = cv2.GaussianBlur(original_image, (21, 21), 0)
        output_image = np.where(np.stack([pred_mask_resized]*3, axis=-1) == 1, original_image, blurred_bg)

    elif effect == "anonymize":
        # Ensure correct color channels for pixelation
        subject_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        pixelated_subject = cv2.resize(subject_rgb, (32, 32), interpolation=cv2.INTER_LINEAR)
        pixelated_subject = cv2.resize(pixelated_subject, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)
        pixelated_subject_bgr = cv2.cvtColor(pixelated_subject, cv2.COLOR_RGB2BGR) # Convert back if needed by np.where
        output_image = np.where(np.stack([pred_mask_resized]*3, axis=-1) == 1, pixelated_subject_bgr, original_image)
    else:
        output_image = original_image

    # 5. Encode final image to bytes and return
    # Convert final image from RGB to BGR before encoding with OpenCV
    final_image_bgr = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
    _, encoded_img = cv2.imencode(".png", final_image_bgr)
    return io.BytesIO(encoded_img.tobytes())