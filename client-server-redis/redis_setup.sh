#!/bin/bash

sudo apt-get update

# Install Redis Dependencies
sudo apt-get install libjemalloc-dev -y
sudo apt-get install libgtest-dev -y
sudo apt install redis-tools

# Install OpenSSL Library to enable TLS support (not sure what TLS is)
sudo apt-get install libssl-dev -y

# Running tests with TLS support 
sudo apt-get install tcl-tls -y

sudo apt install tcl -y 

# tclsh --version

# Install Redis Source Code
git clone https://github.com/redis/redis.git

# Change directory to Redis
cd redis

# Build Redis 
make BUILD_TLS=yes

# Test Redis
# ./utils/gen-test-certs.sh
# ./runtest --tls

# To start the server: ./redis-server --port 9999 --protected-mode no
# In the client: redis-cli -h <IP Address> -p <Port Number>
# For example: redis-cli -h 128.105.145.101 -p 9999
