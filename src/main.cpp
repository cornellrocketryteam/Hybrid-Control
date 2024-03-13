#ifndef USE_LABJACK
#define USE_LABJACK
#endif
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
    std::thread read(&Controller::read, &c, std::ref(running));

    run.join();
    read.join();

    CloseOrDie(handle);
    WaitForUserIfWindows();

    return 0;
}