#include "kernel/kernel.h"
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;

    Kernel kernel;
    kernel.initialize();
    kernel.run();
    kernel.shutdown();
    
    return 0;
}


