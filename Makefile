CXX = g++
CXXFLAGS = -Wall --std=c++11
TEST_NAME = digitalEqTest
INCLUDE_DIR = ./include
SOURCES = ./src/digitalEq.cpp ./test/digitalEqTest.cpp

digitalTestEq.o:
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -o ./bin/$(TEST_NAME) -I$(INCLUDE_DIR) $(SOURCES)

all: digitalTestEq.o

clean:
	rm -rf ./bin/*
