CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = kernel_main
SRCDIR = .
SOURCES = $(wildcard *.cpp) $(wildcard kernel/*.cpp)
OBJECTS = $(SOURCES:.cpp=.o)
INCLUDES = -I.

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

