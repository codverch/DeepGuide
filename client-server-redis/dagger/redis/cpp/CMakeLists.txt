PREPEND(PREP_SOURCES ${ROOT_DIR} ${SOURCES})

# Find the relevant Redis Makefile

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
message(STATUS "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
SET(REDIS_MAKE_CMD REDIS_CFLAGS="-I${CMAKE_CURRENT_SOURCE_DIR}/cpp"
                   REDIS_CFLAGS+="-I${CMAKE_CURRENT_BINARY_DIR}"
                   REDIS_CFLAGS+="-I${CMAKE_CURRENT_SOURCE_DIR}/redis/src"
                   REDIS_CFLAGS+="-I${CMAKE_CURRENT_SOURCE_DIR}/../../src"
                   REDIS_LDFLAGS="-L${CMAKE_CURRENT_BINARY_DIR}"
                   LDFLAGS="-L${CMAKE_CURRENT_BINARY_DIR}"
                   LIBS="-ldagger-redis"
                   LIBS+="-lhugetlbfs"
                   LIBS+="-levent"
                   LIBS+="-pthread"
                   MALLOC=libc)
message(STATUS "REDIS_MAKE_CMD: ${REDIS_MAKE_CMD}")
message(STATUS "Current Redis Build Directory: ${CMAKE_CURRENT_BINARY_DIR}")

# Manually: change the redis makefile so that it includes dagger 

add_custom_target(redis_server ALL
                  /usr/bin/make -f "${CMAKE_CURRENT_SOURCE_DIR}/redis/src/Makefile" ${REDIS_MAKE_CMD}
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/redis/src
                )
