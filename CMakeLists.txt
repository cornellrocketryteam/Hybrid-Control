cmake_minimum_required(VERSION 3.27)

project(hybrid C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

find_package(Curses REQUIRED)
include_directories(${CURSES_INCLUDE_DIR})


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
)

# Add all executables
add_executable(${PROJECT_NAME}
    ${SOURCES}
)

target_link_libraries(${PROJECT_NAME} ${CURSES_LIBRARIES})

