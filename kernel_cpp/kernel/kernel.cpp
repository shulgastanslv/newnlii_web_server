#include "kernel.h"
#include <iostream>

Kernel::Kernel() : is_initialized(false) {
}

Kernel::~Kernel() {
    if (is_initialized) {
        shutdown();
    }
}

void Kernel::initialize() {
    if (!is_initialized) {
        std::cout << "Kernel: Initializing..." << std::endl;
        is_initialized = true;
        std::cout << "Kernel: Initialized successfully!" << std::endl;
    }
}

void Kernel::run() {
    if (is_initialized) {
        std::cout << "Kernel: Running..." << std::endl;
        std::cout << "Kernel: Hello from kernel!" << std::endl;
    } else {
        std::cerr << "Kernel: Error - Kernel not initialized!" << std::endl;
    }
}

void Kernel::shutdown() {
    if (is_initialized) {
        std::cout << "Kernel: Shutting down..." << std::endl;
        is_initialized = false;
        std::cout << "Kernel: Shutdown complete!" << std::endl;
    }
}

