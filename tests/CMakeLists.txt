cmake_minimum_required(VERSION 3.15)
project(test C CXX)

# Find and include Curses
find_package(Curses REQUIRED)
include_directories(${CURSES_INCLUDE_DIRS})

# Add executable and sources
add_executable(test on_off.cpp)

# Add subdirectory for additional libraries (if needed)
add_subdirectory(lib)

# Include directories
target_include_directories(test PRIVATE ${CMAKE_SOURCE_DIR} /usr/local/include)

# Link directories and libraries
target_link_directories(test PRIVATE /usr/local/lib)
target_link_libraries(test PRIVATE LabJackM ${CURSES_LIBRARIES})
