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

void read(int handle);

int main(int argc, char *argv[]) {

    int handle = -1;

#ifdef USE_LABJACK
    int err = LJM_Open(LJM_dtT7, LJM_ctANY, "LJM_idANY", &handle);
    ErrorCheck(err, "LJM_Open");
#endif

    Controller c = Controller(handle);
    std::thread run(&Controller::run, &c);
    std::thread read(&Controller::read, &c);

    run.join();
    read.join();

    return 0;
}