import json
from google.protobuf.json_format import ParseDict, MessageToDict

from genesys_pb2 import(
    GenModelRequest,
) 

FILE_NAME = "./sample_inputs/simple_battery.json"

def read_json_into_proto(file_name):
    with open(file_name) as file:
        input_dict = json.load(file)

    request = ParseDict(
        js_dict = input_dict,
        message= GenModelRequest(),
        ignore_unknown_fields=False
    )
    return request

def instantiate_model():
    model = read_json_into_proto(FILE_NAME)

    return model