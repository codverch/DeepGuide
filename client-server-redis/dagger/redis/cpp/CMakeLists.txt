PREPEND(PREP_SOURCES ${ROOT_DIR} ${SOURCES})

# Generate RPC stubs
SET(KVS_IDL_FILENAME ${CMAKE_CURRENT_SOURCE_DIR}/../kvs_client/kvs.dproto)
execute_process(COMMAND python3 rpc_gen.py ${KVS_IDL_FILENAME} ${CMAKE_CURRENT_BINARY_DIR}
                WORKING_DIRECTORY ${RPC_CODEGEN_PATH}
                RESULT_VARIABLE STUB_CODEGEN_RESULT)
if(NOT STUB_CODEGEN_RESULT EQUAL "0")
        message(FATAL_ERROR "failed to generate RPC stubs")
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR})
link_directories(${CMAKE_CURRENT_BINARY_DIR})

# Build a special ldagger for redis that contains cpp wrapper symbols
add_library(dagger-redis SHARED ${PREP_SOURCES} cpp/redis_cpp_wrapper.cc)
target_compile_definitions(dagger-redis PRIVATE PROFILE_LATENCY=1)
target_link_libraries(dagger-redis ${FPGA_LIBS} ${LIBRARIES} -shared)

# Build redis server
SET(REDIS_MAKE_CMD CPPFLAGS="-I${CMAKE_CURRENT_SOURCE_DIR}/cpp"
                       CPPFLAGS+="-I${CMAKE_CURRENT_BINARY_DIR}"
                       CPPFLAGS+="-I${CMAKE_CURRENT_SOURCE_DIR}/../../src"
                       LDFLAGS="-L${CMAKE_CURRENT_BINARY_DIR}"
                       LIBS="-ldagger-redis"
                       LIBS+="-lhugetlbfs"
                       LIBS+="-levent"
                       LIBS+="-pthread")

add_custom_target(redis_server ALL
                  COMMAND /usr/bin/make ${REDIS_MAKE_CMD}
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/redis)
