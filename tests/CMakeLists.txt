cmake_minimum_required(VERSION 3.15)
project(EXAMPLE C CXX)

find_package(Curses REQUIRED)
include_directories(${CURSES_INCLUDE_DIR})

add_executable(test stream_data.cpp)
target_include_directories(test PRIVATE ${CMAKE_SOURCE_DIR} /usr/local/include)
target_link_directories(test PRIVATE /usr/local/lib)
target_link_libraries(test PRIVATE LabJackM ${CURSES_LIBRARIES})