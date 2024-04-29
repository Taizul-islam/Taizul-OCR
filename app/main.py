from fastapi import FastAPI, File, UploadFile
import easyocr
import os
import multipart

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World 11"}


@app.post("/")
async def root(uploaded_file: UploadFile = File(...)):
    file_location = f"file/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    h = []
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_location)

    for (bbox, text, prob) in result:
        h.append(text)
        print(f'Text: {text}, Probability: {prob} {bbox}')

    os.remove(file_location)

    return {"result": h}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
