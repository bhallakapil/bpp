CC = clang++
CFLAGS = -O3 -flto -mtune=generic -std=c++11 -fPIC -DDDS_THREADS_GCD -DDDS_THREADS_STL
LDFLAGS = -dynamiclib -fPIC

SOURCES = ABsearch.cpp ABstats.cpp CalcTables.cpp DealerPar.cpp File.cpp Init.cpp LaterTricks.cpp Memory.cpp \
          Moves.cpp Par.cpp PlayAnalyser.cpp PBN.cpp QuickTricks.cpp Scheduler.cpp SolveBoard.cpp SolverIF.cpp \
          System.cpp ThreadMgr.cpp Timer.cpp TimerGroup.cpp TimerList.cpp TimeStat.cpp TimeStatList.cpp \
          TransTableS.cpp TransTableL.cpp dds.cpp dump.cpp

OBJECTS = $(SOURCES:.cpp=.o)

all: libdds.a libdds.dylib

libdds.a: $(OBJECTS)
	ar rcs libdds.a $(OBJECTS)

libdds.dylib: $(OBJECTS)
	$(CC) $(LDFLAGS) -o libdds.dylib $(OBJECTS)

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) libdds.a libdds.dylib
