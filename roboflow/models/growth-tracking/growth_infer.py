import os
from inference_sdk import InferenceHTTPClient

API_KEY = os.getenv("ROBOFLOW_API_KEY")

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY,
)

result = CLIENT.infer("your_image.jpg", model_id="growth-stage-pwxza/2")
