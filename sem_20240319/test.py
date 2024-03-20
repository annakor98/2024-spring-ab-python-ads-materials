import requests
import json
from mlserver.types import InferenceResponse
from mlserver.codecs.string import StringRequestCodec

inputs = {
    "flowers": [[0, 0, 0, 0], [7, 3.2, 4.7, 1.4], [6.2, 3.4, 5.4, 2.3]]
}

inputs_string = json.dumps(inputs)

inference_request = {
    "inputs": [
        {
            "name": "echo_request",
            "shape": [len(inputs_string)],
            "datatype": "BYTES",
            "data": [inputs_string],
        }
    ]
}

inference_url = "http://localhost:9000/v2/models/iris-predictor/infer"

response = requests.post(inference_url, json=inference_request)
print(response)

inference_response = InferenceResponse.parse_raw(response.text)
raw_json = StringRequestCodec.decode_response(inference_response)
output = json.loads(raw_json[0])
print(output)