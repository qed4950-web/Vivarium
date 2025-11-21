import os
from inference_sdk import InferenceHTTPClient

API_KEY = os.getenv("ROBOFLOW_PRIVATE_KEY") or os.getenv("ROBOFLOW_API_KEY")

if not API_KEY:
    raise ValueError("Set ROBOFLOW_PRIVATE_KEY (preferred) or ROBOFLOW_API_KEY.")

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY,
)

result = client.infer("your_image.jpg", model_id="pest-detection-ntbss/1")
print(result)
