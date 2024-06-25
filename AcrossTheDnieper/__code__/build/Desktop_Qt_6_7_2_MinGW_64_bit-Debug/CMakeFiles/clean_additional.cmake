# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\__code___autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\__code___autogen.dir\\ParseCache.txt"
  "__code___autogen"
  )
endif()
