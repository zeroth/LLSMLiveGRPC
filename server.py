from concurrent import futures
from os import name

import grpc
import llsm_post_process_pb2
import llsm_post_process_pb2_grpc

import numpy as np
from NDArrayHelper import proto_to_ndarray, ndarray_to_proto

class LLSMPostProcessServicer(llsm_post_process_pb2_grpc.LLSMPostProcessServicer):

    def __init__(self) -> None:
        super().__init__()
    
    def GetList(self, request, context):
        return llsm_post_process_pb2.AvailableServices(services=["Ping", "Pong"])
    
    def GetZStackMaxIntensity(self, request, context):
        np_array = proto_to_ndarray(request)
        return ndarray_to_proto(np.max(np_array, axis=0))


def serve():
    server = grpc.server(thread_pool = futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_receive_message_length', -1),
                                ('grpc.max_send_message_length', -1)])
    llsm_post_process_pb2_grpc.add_LLSMPostProcessServicer_to_server(LLSMPostProcessServicer(), 
        server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()