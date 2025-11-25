#ifndef KERNEL_H
#define KERNEL_H

class Kernel {
public:
    Kernel();
    ~Kernel();
    
    void initialize();
    void run();
    void shutdown();
    
private:
    bool is_initialized;
};

#endif

