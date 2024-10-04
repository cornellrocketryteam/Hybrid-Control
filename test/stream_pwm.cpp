#include <LJMUtil.hpp>
#include <LabJackM.h>
#include <stdio.h>
#include <vector>

int main() {
    int err, handle;

    double INIT_SCAN_RATE = 70;
    int SCANS_PER_READ = 1;

    enum { NUM_CHANNELS = 14 };

    int *aScanList = new int[NUM_CHANNELS];

    handle = OpenOrDie(LJM_dtANY, LJM_ctANY, "LJM_idANY");

    err = LJM_InitializeAperiodicStreamOut(handle, 0, 2500, 70);

    const char *aName = "FIO_STATE";
    double aValue = 32386;  // 11111101 0000010 - FIO1 being targeted
    int numFrames = 1;

    err = LJM_eWriteName(handle, aName, aValue);

    err = LJM_eStreamStart(handle, SCANS_PER_READ, 1, aScanList, &INIT_SCAN_RATE);

    int samplesToWrite = 200;
    std::vector<double> writeData;
    
    for (int i = 0; i < samplesToWrite; ++i) {
        writeData.push_back(0);
        writeData.push_back(3);
    }

    int queueVals;

    err = LJM_WriteAperiodicStreamOut(handle, 0, writeData.size(), writeData.data(), &queueVals);

    while (true) {

    }

    return 0;
}