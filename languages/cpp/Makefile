.PHONY: all build clean run test

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
LDFLAGS = -lssl -lcrypto

SRC = crypto_utils.cpp
TARGET = crypto_utils

all: build

build:
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

run: build
	./$(TARGET)

clean:
	rm -f $(TARGET)

test: build
	./$(TARGET)

help:
	@echo "Available targets:"
	@echo "  build  - Compile the program"
	@echo "  run    - Compile and run"
	@echo "  clean  - Remove binary"
	@echo "  test   - Run the program"
