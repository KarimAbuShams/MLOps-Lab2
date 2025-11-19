from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
from mylib.logic import predict_image_class, resize_image

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Carga el home.html (Punto 21 del PDF)
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Leemos los bytes del archivo subido
        contents = await file.read()
        # Convertimos bytes a imagen PIL
        image = Image.open(io.BytesIO(contents))
        
        prediction = predict_image_class(image)
        return {"filename": file.filename, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resize")
async def resize(
    file: UploadFile = File(...), 
    width: int = Form(...), 
    height: int = Form(...)
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        resized_image = resize_image(image, width, height)
        
        return {
            "filename": file.filename, 
            "original_size": image.size,
            "new_size": resized_image.size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
