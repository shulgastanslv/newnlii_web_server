cmake_minimum_required(VERSION 3.10)
project(KernelProject)

# Установка стандарта C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Добавление исполняемого файла
add_executable(kernel_main
    main.cpp
    kernel/kernel.cpp
)

# Включение директорий для заголовочных файлов
target_include_directories(kernel_main PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

