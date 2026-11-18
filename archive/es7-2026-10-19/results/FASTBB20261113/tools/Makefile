# Build fastbb (phase 1) and fastbb2 (phase 2: fastbb + the slice rule, --slice=1).
# No third-party code; only zlib for the .json.gz output.
#   make BUILD=/home/jay/research/data/fastbb-20261113/build            (fastbb)
#   make BUILD=/home/jay/research/data/fastbb-20261113/p2/bin fastbb2    (fastbb2)
CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -march=native -fopenmp-simd -pthread -Wall -Wextra -Wno-unused-parameter
BUILD ?= .
$(BUILD)/fastbb: fastbb.cpp
	$(CXX) $(CXXFLAGS) -o $@ fastbb.cpp -lz
.PHONY: fastbb2
fastbb2: $(BUILD)/fastbb2
$(BUILD)/fastbb2: fastbb2.cpp
	$(CXX) $(CXXFLAGS) -o $@ fastbb2.cpp -lz
