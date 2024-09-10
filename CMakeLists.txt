cmake_minimum_required(VERSION 3.27)
project(hybrid C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_VERBOSE_MAKEFILE TRUE)

# Include curses
include_directories(${CURSES_INCLUDE_DIR})
include_directories("/usr/local/include/")

find_package(Curses REQUIRED)
add_definitions(-DUSE_LABJACK)

# Add compiler flags and definitions
add_compile_options(
    -Wall
    -Wno-format
    -Wno-unused-function
)

# Add source files from src/
set(SOURCES
    src/main.cpp
    src/test_stand.cpp
    src/controller.cpp
    src/view.cpp
    src/config.cpp
)

# Add all executables
add_executable(${PROJECT_NAME}
    ${SOURCES}
)

add_subdirectory(lib)

# Link curses library
target_link_libraries(${PROJECT_NAME} ${LJM_LIBRARY} ${CURSES_LIBRARIES})