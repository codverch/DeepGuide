#!/bin/bash

# Clone the mica2 repository
git clone https://github.com/efficient/mica2.git
cd mica2

# Download and extract dpdk
# Reference used to build dpdk: https://core.dpdk.org/doc/quick-start/
# Downloaded dpdk from https://core.dpdk.org/download/
wget https://fast.dpdk.org/rel/dpdk-16.11.11.tar.xz
tar xf dpdk-16.11.11.tar.xz
cd dpdk-stable-16.11.11

# Build dpdk
sudo apt-get install meson -y
make config T=x86_64-native-linuxapp-gcc
make -j

# Install dependencies
sudo apt-get update
sudo apt-get install -y g++-5
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 100
sudo update-alternatives --config g++
sudo apt-get install -y cmake
sudo apt-get install -y make
sudo apt-get install -y libnuma-dev
sudo apt-get install -y libcurl4-openssl-dev
sudo apt-get install -y libsqlite3-dev

# Enable SQLite option in cmake
cmake -DSQLITE=ON ..

# Install etcd-server
sudo apt-get install -y etcd-server

# Verify Python version (should be greater than 3.4)
python3 --version

# Navigate back to the mica2 directory
cd ..

# Add the DPDK include directory to CMakeLists.txt
sed -i '/INCLUDE_DIRECTORIES(/a \    INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/dpdk-stable-16.11.11)' CMakeLists.txt


# Build mica2
cd build
ln -s ../dpdk-stable-16.11.11 ./dpdk
cmake ..
make -j

# Set up mica2 environment
ln -s ../src/mica/test/*.json .
../script/setup.sh 8192 8192    # 2 NUMA nodes, 16 Ki pages (32 GiB)

# Stop and start etcd
sudo systemctl stop etcd
sudo systemctl start etcd


# Errors and how to fix them

# CMakeFiles/Makefile2:178: recipe for target 'CMakeFiles/test_rand.dir/all' failed
# make[1]: *** [CMakeFiles/test_rand.dir/all] Error 2
# cc1plus: fatal error: rte_config.h: No such file or directory

# Solution: In mica2/CMakeLists.txt, add the following line: include_directories(${CMAKE_SOURCE_DIR}/dpdk-stable-16.11.11)
