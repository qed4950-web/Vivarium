from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="DjJLiZqgSldm5TR0LBX0"
)

result = CLIENT.infer(your_image.jpg, model_id="growth-stage-pwxza/2")