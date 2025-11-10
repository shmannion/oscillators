# === Python configuration ===
PYTHON_CONFIG   := /opt/homebrew/bin/python3-config
PYTHON_INCLUDE  := $(shell $(PYTHON_CONFIG) --includes)

# === Compiler setup ===
CXX       := clang++
CXXFLAGS  := -std=c++17 -O3 -Wall -fPIC $(PYTHON_INCLUDE) -Iinclude
LDFLAGS   := -bundle -undefined dynamic_lookup

# === Project structure ===
SRC_DIRS  := $(shell find src -type d)
SRC_ALL   := $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.cpp))
OBJ_DIR   := obj
PYTHON_DIR := python
TEST_DIR  := test

# === Source groups ===
SRC_PY    := $(filter %/py_%.cpp,$(SRC_ALL))                 # Python wrappers
SRC_CORE  := $(filter-out %/py_%.cpp %/main.cpp,$(SRC_ALL))  # Core C++ (used by both)
TEST_SRC  := src/main.cpp

# === Object files ===
OBJ_PY    := $(patsubst src/%.cpp,$(OBJ_DIR)/%.o,$(SRC_PY) $(SRC_CORE))
TEST_OBJ  := $(OBJ_DIR)/main.o

# === Targets ===
TARGET_SO := oscillators.so
TEST_MAIN := $(TEST_DIR)/main

# === Phony targets ===
.PHONY: all clean test copy_so

# === Default build ===
all: $(TARGET_SO) $(TEST_MAIN) copy_so

# === Build Python module (.so) ===
$(TARGET_SO): $(OBJ_PY)
	$(CXX) -o $@ $(OBJ_PY) $(LDFLAGS)

# === Compile rule for all .cpp ===
$(OBJ_DIR)/%.o: src/%.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# === Copy .so to python/ ===
copy_so: $(TARGET_SO)
	mkdir -p $(PYTHON_DIR)
	cp $(TARGET_SO) $(PYTHON_DIR)/

# === Build standalone test program ===
$(TEST_MAIN): $(TEST_OBJ) $(filter-out $(OBJ_DIR)/py/%.o,$(OBJ_PY))
	mkdir -p $(TEST_DIR)
	$(CXX) -o $@ $^

# === Run C++ test ===
test: $(TEST_MAIN)
	./$(TEST_MAIN)

# === Clean ===
clean:
	rm -rf $(OBJ_DIR) $(TARGET_SO) $(PYTHON_DIR)/$(TARGET_SO) $(TEST_MAIN)

