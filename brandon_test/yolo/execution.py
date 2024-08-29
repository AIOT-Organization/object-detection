
import torch
import cv2

model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache



img = cv2.imread('CurveLane.png')
results = model(img, size=640)  # reduce size=320 for faster inference
final_res = results.pandas().xyxy[0].to_json(orient="records")

print(final_res)



# #Swap with Python file Read
# '''
# image_file = request.files["image"]
# image_bytes = image_file.read()
# '''
# img = Image.open(io.BytesIO(image_bytes))

