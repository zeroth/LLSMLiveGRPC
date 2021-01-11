from __future__ import print_function

# import random
# import logging
import time

import grpc
import llsm_post_process_pb2
import llsm_post_process_pb2_grpc
import numpy as np
import tifffile
from NDArrayHelper import proto_to_ndarray, ndarray_to_proto

def get_processes(stub):
    processes = stub.GetList(llsm_post_process_pb2.Empty())
    print(type(processes))
    # for process in processes:
    print(processes.services)

def get_z_max_intensity(stub):
    start_time = time.time()
    img = tifffile.imread('./test.tif')
    max_int_nd = stub.GetZStackMaxIntensity(ndarray_to_proto(img))
    return_img = proto_to_ndarray(max_int_nd)
    print("return_img.shape", return_img.shape)
    tifffile.imwrite("./max_int_test.tif", data=return_img)
    elapsed_time = time.time() - start_time
    print("total time taken in sec ", elapsed_time)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(target='localhost:50051',
                                options=[('grpc.max_receive_message_length', -1),
                                ('grpc.max_send_message_length', -1)]) as channel:
        stub = llsm_post_process_pb2_grpc.LLSMPostProcessStub(channel)
        print("-------------- get_processes --------------")
        get_processes(stub)
        print("-------------- get_z_max_intensity --------------")
        get_z_max_intensity(stub)
        # print("-------------- ListFeatures --------------")
        # guide_list_features(stub)
        # print("-------------- RecordRoute --------------")
        # guide_record_route(stub)
        # print("-------------- RouteChat --------------")
        # guide_route_chat(stub)

if __name__ == "__main__":
    # logging.basicConfig()
    run()