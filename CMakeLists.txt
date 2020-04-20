CMAKE_MINIMUM_REQUIRED(VERSION 2.8.5)

#---------------------------------------------------------------
# Load macros and functions for Elements-based projects. The find_package
# function detects the ElementsProjectConfig.cmake file.
find_package(ElementsProject)
#---------------------------------------------------------------

# Declare project name and version

elements_project(Primal 1.8.0 DESCRIPTION "Lensy Strong Device" USE Elements 5.10.0)
