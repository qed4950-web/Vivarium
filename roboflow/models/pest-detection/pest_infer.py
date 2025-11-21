from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ROBOFLOW_API_KEY"
)

result = client.infer("your_image.jpg", model_id="pest-detection-ntbss/1")
print(result)
