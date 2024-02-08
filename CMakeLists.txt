cmake_minimum_required(VERSION 3.27)
project(hybrid C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_VERBOSE_MAKEFILE FALSE)

# add_definitions(-DUSE_LABJACK)

# set(LIB_FILES lib/LJM_Utilities.h lib/LJM_StreamUtilities.h)
# set(LIB_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lib")
# set(LIB_SRCS ${LIB_SRCS} "${LIB_FILES}")
# add_library(${LIB} ${LIB_SRCS})


# Include curses and the LabJack library
include_directories("/usr/local/include/")
include_directories(${CURSES_INCLUDE_DIR})


set(LJM_LIBRARY "/usr/local/lib/libLabJackM.dylib")
find_package(Curses REQUIRED)


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

# Add external libraries
add_subdirectory(${PROJECT_SOURCE_DIR}/lib)

# Link library directories
target_link_directories(${PROJECT_NAME} 
    PRIVATE
    ${PROJECT_SOURCE_DIR}/lib
)

# Include library headers
target_include_directories(${PROJECT_NAME}
    PRIVATE
    ${PROJECT_SOURCE_DIR}/lib
)

# Link curses and the LabJack library
target_link_libraries(${PROJECT_NAME} ${LJM} ${LJM_LIBRARY} ${CURSES_LIBRARIES})
