#include "controller.hpp"
#include <LJM_Utilities.h>
#include <LabJackM.h>

int main(int argc, char *argv[]) {

    int handle = -1;

#ifdef USE_LABJACK
    int err = LJM_Open(LJM_dtT7, LJM_ctANY, "LJM_idANY", &handle);
    ErrorCheck(err, "LJM_Open");
#endif

    Controller c = Controller(handle);
    c.run();

    return 0;
}