# C++ Kernel Project

Простой C++ проект с kernel модулем и hello world программой.

## Структура проекта

```
kernel_cpp/
├── main.cpp          # Главный файл с hello world
├── kernel/
│   ├── kernel.h      # Заголовочный файл kernel
│   └── kernel.cpp    # Реализация kernel
├── CMakeLists.txt    # Файл для сборки через CMake
└── Makefile          # Файл для сборки через Make
```

## Сборка

### Использование CMake:

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

### Использование Make:

```bash
make
```

## Запуск

После сборки:

```bash
./kernel_main
```

или

```bash
make run
```

## Очистка

```bash
make clean
```

или для CMake:

```bash
rm -rf build
```

