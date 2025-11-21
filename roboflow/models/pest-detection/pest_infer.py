import os
from inference_sdk import InferenceHTTPClient

API_KEY = os.getenv("ROBOFLOW_API_KEY")

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY,
)

result = client.infer("your_image.jpg", model_id="pest-detection-ntbss/1")
print(result)
