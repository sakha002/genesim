import logging
import sys
import os
import grpc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protobuf/generated')))

from genesys_pb2_grpc import(
    GenModelServiceStub
)

from model import instantiate_model

def create_stub(channel):
    stub = GenModelServiceStub(channel)
    return stub


def send_request(channel, request):
    stub = create_stub(channel)
    response = stub.OptimizeAsset(request)
    logging.info("client received response")
    return  response


if __name__ == "__main__":

    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:50051'


    request = instantiate_model()

    logging.info("client instantiated model")
    # credentials = grpc.ssl_channel_credentials()
    # with grpc.secure_channel(target, credentials) as channel:
    #     response = send_request(channel, request)

    with grpc.insecure_channel(target) as channel:
        response = send_request(channel, request)
