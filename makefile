# ==============================

# Python configuration
PYTHON_CONFIG   := python3-config
PYTHON_INCLUDE  := $(shell $(PYTHON_CONFIG) --includes)
PYTHON_LDFLAGS  := $(shell $(PYTHON_CONFIG) --ldflags)

# Compiler setup
CXX       := g++
CXXFLAGS  := -std=c++17 -O3 -Wall -fPIC $(PYTHON_INCLUDE) -Iinclude
LDFLAGS   := -shared $(PYTHON_LDFLAGS)

# Project structure
SRC_DIRS  := $(shell find src -type d)
SRC_ALL   := $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.cpp))
OBJ_DIR   := obj

# Collect all .cpp files under src/
SRC_PY    := $(filter %/py_%.cpp,$(SRC_ALL))
SRC_CORE  := $(filter-out %/py_%.cpp %/main.cpp,$(SRC_ALL))
SRC_MAIN  := src/main.cpp
OBJ_PY    := $(patsubst src/%.cpp,$(OBJ_DIR)/%.o,$(SRC_PY) $(SRC_CORE))
OBJ_MAIN  := $(patsubst src/%.cpp,$(OBJ_DIR)/%.o,$(SRC_CORE) $(SRC_MAIN))

TARGET_SO   := oscillators.so
TARGET_BIN  := main
PYTHON_DIR  := python
# Default target
.PHONY: all clean

all: $(TARGET_SO) $(TARGET_BIN) copy_so

# Build Python module
$(TARGET_SO): $(OBJ_PY)
	$(CXX) $(OBJ_PY) -o $@ $(LDFLAGS)

# Build standalone executable
$(TARGET_BIN): $(OBJ_MAIN)
	$(CXX) $(OBJ_MAIN) -o $@

copy_so: $(TARGET_SO)
	mkdir -p $(PYTHON_DIR)
	cp $(TARGET_SO) $(PYTHON_DIR)/

# Compile step
$(OBJ_DIR)/%.o: src/%.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean
clean:
	rm -rf $(OBJ_DIR) $(TARGET_SO) $(TARGET_BIN) $(PYTHON_DIR)/$(TARGET_SO)

