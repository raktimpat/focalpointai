from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from model_processing import process_image

app = FastAPI(title="FocalPoint AI")

@app.post("/segment/")
async def segment_image(effect: str = Form(...), file: UploadFile = File(...)):
    image_bytes = await file.read()
    processed_image_io = process_image(image_bytes, effect)
    return StreamingResponse(processed_image_io, media_type="image/png")

@app.get("/")
def read_root():
    return {"message": "Welcome to FocalPoint AI API (DeepLabV3)"}