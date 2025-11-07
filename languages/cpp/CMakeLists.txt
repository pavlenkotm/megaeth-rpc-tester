cmake_minimum_required(VERSION 3.10)
project(Web3CryptoUtils)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenSSL
find_package(OpenSSL REQUIRED)

# Add executable
add_executable(crypto_utils crypto_utils.cpp)

# Link OpenSSL
target_link_libraries(crypto_utils OpenSSL::SSL OpenSSL::Crypto)

# Compiler warnings
if(MSVC)
    target_compile_options(crypto_utils PRIVATE /W4)
else()
    target_compile_options(crypto_utils PRIVATE -Wall -Wextra -Wpedantic)
endif()

# Installation
install(TARGETS crypto_utils DESTINATION bin)
