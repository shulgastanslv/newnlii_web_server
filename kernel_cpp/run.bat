@echo off
echo ========================================
echo Starting Kernel Project...
echo ========================================

@echo build_kernel
cmake --build build --config Debug
@echo kernel_built

@echo run_kernel
.\build\Debug\kernel_main.exe