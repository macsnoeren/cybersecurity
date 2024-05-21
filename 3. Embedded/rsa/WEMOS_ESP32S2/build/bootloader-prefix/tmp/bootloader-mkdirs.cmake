# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Users/macsnoer/esp/v5.2.1/esp-idf/components/bootloader/subproject"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/tmp"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/src"
  "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Data/projects/ESPIDFESPS2TEST/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
