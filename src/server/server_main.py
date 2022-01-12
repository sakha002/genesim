from concurrent.futures import ThreadPoolExecutor
import logging
import grpc
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../protobuf/generated')))

from genesys_pb2_grpc import(
    add_GenModelServiceServicer_to_server
)

from genesys_server import GenModelServer


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)



def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=200), maximum_concurrent_rpcs=100)
    
    add_GenModelServiceServicer_to_server(GenModelServer(), server)
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info('GeneSys server ready on port %r', port)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
