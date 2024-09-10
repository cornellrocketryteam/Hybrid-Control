#include "LJMUtil.hpp"
#include "controller.hpp"
#include <LabJackM.h>
#include <fstream>
#include <iostream>
#include <signal.h>
#include <sstream>
#include <thread>

int main(int argc, char *argv[]) {

    int handle = -1;
    bool running = true;

#ifdef USE_LABJACK
    int err = LJM_Open(LJM_dtT7, LJM_ctANY, "LJM_idANY", &handle);
    ErrorCheck(err, "LJM_Open");
#endif

    Controller c = Controller(handle);
    std::thread run(&Controller::run, &c, std::ref(running));
#ifdef USE_LABJACK
    std::thread read(&Controller::read, &c, std::ref(running));
#endif

    run.join();
#ifdef USE_LABJACK
    read.join();
#endif

    CloseOrDie(handle);

    return 0;
}