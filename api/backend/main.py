# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# import cv2

# app = FastAPI()

# # Initialize camera
# camera = cv2.VideoCapture(0)  # Use 0 for built-in webcam, or a filename to read from a file

# def generate_frames():
#     while True:  # Adding a while loop here
#         # Capture frame-by-frame
#         success, frame = camera.read()
#         if not success:
#             break  # Now 'break' is inside a loop
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.get("/stream.m3u8")
# async def get_m3u8():
#     return FileResponse("./static/stream.m3u8", media_type="application/vnd.apple.mpegurl")

# @app.get("/stream/{segment}.ts")
# async def get_ts(segment: str):
#     return FileResponse(f"./static/{segment}.ts", media_type="video/MP2T")

# @app.get("/video")
# async def video_feed():
#     return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse,StreamingResponse
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# # CORS middleware settings
# origins = [
#     "http://localhost:3000",  # React app
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Serve static files
# app.mount("/static", StaticFiles(directory="./static/"), name="static")

# @app.get("/stream")
# async def video_endpoint():
#     video_path = "./static/output.m3u8"
#     def iterfile():
#         with open(video_path, mode="rb") as file_like:
#             yield from file_like

#     return StreamingResponse(iterfile(), media_type="video/mp4")


from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
# CORS middleware settings
origins = [
    "http://localhost:3001",  # React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stream/{filename}")
def get_file(filename: str):
    valid_extensions = ["m3u8", "ts"]
    file_ext = filename.split(".")[-1]
    if file_ext not in valid_extensions:
        return {"error": "Invalid file type"}
        
    filepath = f"./static/{filename}"
    if os.path.exists(filepath):
        media_type = "application/vnd.apple.mpegurl" if file_ext == "m3u8" else "video/MP2T"
        return FileResponse(filepath, media_type=media_type)
    else:
        return {"error": "File not found"}

