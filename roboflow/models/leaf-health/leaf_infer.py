from inference_sdk import InferenceHTTPClient
import os

API_KEY = os.getenv("ROBOFLOW_API_KEY")

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
)

def predict_leaf_health(image_path):
    result = client.infer(image_path, model_id="leaf-disease-e34h5/1")
    return result
