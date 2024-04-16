#!/bin/bash

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
