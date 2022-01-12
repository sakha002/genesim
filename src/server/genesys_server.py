import logging 

from genesys_pb2_grpc import GenModelServiceServicer

from genesys_pb2 import GenSolutionResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class GenModelServer(GenModelServiceServicer):

    def OptimizeAsset(self, request, context):

        response = GenSolutionResponse()
        return response

