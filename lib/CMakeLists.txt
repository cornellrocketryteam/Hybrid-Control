cmake_minimum_required(VERSION 3.27)

add_library(LJM INTERFACE)

target_sources(LJM INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/LJM_Utilities.cpp
    ${CMAKE_CURRENT_LIST_DIR}/LJM_StreamUtilities.cpp
)