cmake_minimum_required(VERSION 3.27)

project(hybrid C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# add_definitions(-DUSE_LABJACK)

set(LJM_LIBRARY "/usr/local/lib/libLabJackM.dylib")
find_package(Curses REQUIRED)

# Include curses and the LabJack library
include_directories("/usr/local/include/")
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
    src/config.cpp
    src/LJM_Utilities.cpp
    src/LJM_StreamUtilities.cpp
)

# Add all executables
add_executable(${PROJECT_NAME}
    ${SOURCES}
)

# # Link library directories
# target_link_directories(${PROJECT_NAME} 
#     PRIVATE
#     ${PROJECT_SOURCE_DIR}/lib
# )

# # Include library headers
# target_include_directories(${PROJECT_NAME}
#     PRIVATE
#     ${PROJECT_SOURCE_DIR}/lib
# )

# Link curses and the LabJack library
target_link_libraries(${PROJECT_NAME} ${LJM_LIBRARY} ${CURSES_LIBRARIES})
