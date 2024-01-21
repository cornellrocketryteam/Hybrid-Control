#include <LJM_Utilities.h>
#include <LabJackM.h>
#include <stdio.h>
#include <string.h>

int main() {
    int err;
    int handle;
    int i;

 // Set up for configuring the AIN
 // AIN0:
 //   Negative channel = single ended (199)
 //   Range: +/-10.0 V (10.0).
 //   Resolution index = Default (0)
 //   Settling, in microseconds = Auto (0)
    enum { NUM_FRAMES_CONFIG = 11 };
    const char *aNamesConfig[NUM_FRAMES_CONFIG] =
        {"AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "AIN60_NEGATIVE_CH", "AIN60_RANGE",
         "AIN48_NEGATIVE_CH", "AIN48_RANGE", "AIN49_NEGATIVE_CH", "AIN49_RANGE",
         "AIN0_RANGE", "AIN1_RANGE", "AIN2_RANGE"};
    const double aValuesConfig[NUM_FRAMES_CONFIG] = {199, 10.0, 199, 2.4, 56, 0.1,
                                                     57, 0.1, 10.0, 10.0, 10.0};
    int errorAddress = INITIAL_ERR_ADDRESS;

 // Set up for reading AIN value
    double value = 0;
    const char *NAME = "AIN127";

    enum { NUM_CHANNELS = 14 };
    const char *CHANNEL_NAMES[] = {"AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                                   "AIN3", "AIN1", "AIN2",
                                   "AIN60",
                                   "AIN48", "AIN49"};

 // Open first found LabJack
    handle = OpenOrDie(LJM_dtANY, LJM_ctANY, "LJM_idANY");

    PrintDeviceInfoFromHandle(handle);
    printf("\n");

 // Setup and call eWriteNames to configure AIN0 on the LabJack.
    err = LJM_eWriteNames(handle, NUM_FRAMES_CONFIG, aNamesConfig, aValuesConfig,
                          &errorAddress);
    ErrorCheckWithAddress(err, errorAddress, "LJM_eWriteNames");
    printf("written\n");

    // printf("Set configuration:\n");
    // for (i = 0; i < NUM_FRAMES_CONFIG; i++) {
    //     printf("    %s : %f\n", aNamesConfig[i], aValuesConfig[i]);
    // }

    (void)LJM_eWriteName(handle, "FIO0", 0);
    for (int i = 0; i < 10; i++) {
    }

 // Read AIN0 from the LabJack
    err = LJM_eReadNames(handle, NUM_FRAMES_CONFIG, CHANNEL_NAMES, &value, &errorAddress);
    printf("%d\n", errorAddress);

        // device closed here
    // PrintDeviceInfoFromHandle(handle);
    // printf("\n");
    (void)LJM_eWriteName(handle, "FIO0", 0);
    for (int i = 0; i < 10; i++) {
    }

    ErrorCheck(err, "LJM_eReadName");
    printf("error checked\n");

 // Print results
    printf("\n%s : %f V\n", NAME, value);

    err = LJM_Close(handle);
    printf("%d\n", err);

    WaitForUserIfWindows();

    return LJME_NOERROR;
}
