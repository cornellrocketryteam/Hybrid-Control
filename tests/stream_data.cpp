/**
 * stream_data.cpp: config and stream from multiple AIN channels
 **/

#include "LJM_StreamUtilities.h"
#include <LabJackM.h>
#include <fstream>
#include <stdio.h>
#include <string.h>

void Stream(int handle, int numChannels, const char **channelNames,
            double scanRate, int scansPerRead, int numReads);

void HardcodedConfigureStream(int handle);

int main() {
    int handle;

 // How fast to stream in Hz
    double INIT_SCAN_RATE = 70;

 // How many scans to get per call to LJM_eStreamRead. INIT_SCAN_RATE/2 is
 // recommended
    int SCANS_PER_READ = (int)INIT_SCAN_RATE / 2;

 // How many times to call LJM_eStreamRead before calling LJM_eStreamStop
    const int NUM_READS = 10;

 // Channels/Addresses to stream. NUM_CHANNELS can be less than or equal to
 // the size of CHANNEL_NAMES
    enum { NUM_CHANNELS = 14 };
    const char *CHANNEL_NAMES[] = {"AIN127", "AIN126", "AIN125", "AIN124", "AIN123", "AIN122", "AIN121", "AIN120",
                                   "AIN3", "AIN1", "AIN2",
                                   "AIN60",
                                   "AIN48", "AIN49"};

 // Open first found LabJack
    handle = OpenOrDie(LJM_dtANY, LJM_ctANY, "LJM_idANY");
 // handle = OpenSOrDie("LJM_dtANY", "LJM_ctANY", "LJM_idANY");

    PrintDeviceInfoFromHandle(handle);
    printf("\n");

    Stream(handle, NUM_CHANNELS, CHANNEL_NAMES, INIT_SCAN_RATE, SCANS_PER_READ,
           NUM_READS);

    CloseOrDie(handle);

    WaitForUserIfWindows();

    return LJME_NOERROR;
}

void HardcodedConfigureStream(int handle) {
    // Default Configs
    int err;

    enum { NUM_FRAMES = 10 };
    const char *aNames[] = {"STREAM_TRIGGER_INDEX", "STREAM_CLOCK_SOURCE", "STREAM_RESOLUTION_INDEX",
                            "STREAM_SETTLING_US", "AIN_ALL_RANGE", "AIN_ALL_NEGATIVE_CH",
                            "AIN48_RANGE", "AIN49_RANGE", "AIN48_NEGATIVE_CH", "AIN49_NEGATIVE_CH"};
    const double aValues[] = {0,
                              0,
                              4,
                              1000,
                              10,
                              LJM_GND,
                              0.1, 0.1, 56, 57};

    printf("Writing configurations:\n");
    WriteNamesOrDie(handle, NUM_FRAMES, aNames, aValues);
}

void Stream(int handle, int numChannels, const char **channelNames,
            double scanRate, int scansPerRead, int numReads) {
    int err, iteration, channel;
    int numSkippedScans = 0;
    int totalSkippedScans = 0;
    int deviceScanBacklog = 0;
    int LJMScanBacklog = 0;
    unsigned int receiveBufferBytesSize = 0;
    unsigned int receiveBufferBytesBacklog = 0;
    int connectionType;

    int *aScanList = new int[numChannels];
    unsigned int aDataSize = numChannels * scansPerRead;
    double *aData = new double[sizeof(double) * aDataSize];

    std::ofstream file("test_data.csv");

    err = LJM_GetHandleInfo(handle, NULL, &connectionType, NULL, NULL, NULL, NULL);
    ErrorCheck(err, "LJM_GetHandleInfo");

 // Clear aData. This is not strictly necessary, but can help debugging.
    memset(aData, 0, sizeof(double) * aDataSize);

    err = LJM_NamesToAddresses(numChannels, channelNames, aScanList, NULL);
    ErrorCheck(err, "Getting positive channel addresses");

    HardcodedConfigureStream(handle);

    printf("\n");
    printf("Starting stream...\n");
    err = LJM_eStreamStart(handle, scansPerRead, numChannels, aScanList,
                           &scanRate);
    ErrorCheck(err, "LJM_eStreamStart");
    printf("Stream started. Actual scan rate: %.02f Hz (%.02f sample rate)\n",
           scanRate, scanRate * numChannels);
    printf("\n");

 // Read the scans
    printf("Now performing %d reads\n", numReads);
    printf("\n");
    // change to while + delete numReads and NUM_READS
    for (iteration = 0; iteration < numReads; iteration++) {
        err = LJM_eStreamRead(handle, aData, &deviceScanBacklog,
                              &LJMScanBacklog);
        ErrorCheck(err, "LJM_eStreamRead");

        printf("iteration: %d - deviceScanBacklog: %d, LJMScanBacklog: %d",
               iteration, deviceScanBacklog, LJMScanBacklog);
        if (connectionType != LJM_ctUSB) {
            err = LJM_GetStreamTCPReceiveBufferStatus(handle,
                                                      &receiveBufferBytesSize, &receiveBufferBytesBacklog);
            ErrorCheck(err, "LJM_GetStreamTCPReceiveBufferStatus");
            printf(", receive backlog: %f%%",
                   ((double)receiveBufferBytesBacklog) / receiveBufferBytesSize * 100);
        }
        printf("\n");
        printf("  1st scan out of %d:\n", scansPerRead);
        for (channel = 0; channel < numChannels; channel++) {
            printf("    %s = %0.5f\n", channelNames[channel], aData[channel]);
            file << aData[channel] << ", ";
        }

        file << "\n";

        numSkippedScans = CountAndOutputNumSkippedScans(numChannels,
                                                        scansPerRead, aData);

        if (numSkippedScans) {
            printf("  %d skipped scans in this LJM_eStreamRead\n",
                   numSkippedScans);
            totalSkippedScans += numSkippedScans;
        }
        printf("\n");
    }

    file.close();

    if (totalSkippedScans) {
        printf("\n****** Total number of skipped scans: %d ******\n\n",
               totalSkippedScans);
    }

    printf("Stopping stream\n");
    err = LJM_eStreamStop(handle);
    ErrorCheck(err, "Stopping stream");

    delete[] aData;
    delete[] aScanList;
}