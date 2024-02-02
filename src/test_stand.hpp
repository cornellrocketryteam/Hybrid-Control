#ifndef TEST_STAND_HPP_
#define TEST_STAND_HPP_

#include "config.hpp"
#include <string>
class TestStand {
public:
    /**
     * Sets up the model.
     * @param handle The LabJack handle
     */
    TestStand(int handle);

    /**
     * Turns on a solenoid valve and updates state.
     * @param num The valve to turn on (1-5)
     */
    void sv_on(int num);

    /**
     * Turns off a solenoid valve and updates state.
     * @param num The valve to turn off (1-5)
     */
    void sv_off(int num);

    /**
     * Turns on the MAV and updates state.
     */
    void mav_on();

    /**
     * Turns off the MAV and updates state.
     */
    void mav_off();

    /**
     * The state of all the valves.
     */
    bool sv_states[5] = {false, false, false, false, false};
    bool mav_state = false;

    /**
     * Transitions to a mode and updates the corresponding valves.
     * @param mode The mode to switch to
     */
    void to_mode(Mode mode);

    /**
     * The current mode.
     */
    Mode mode = Mode::default_mode;

    /**
     * The mode that is awaiting confirmation to switch to.
     */
    Mode awaited_mode;

    /**
     * Whether or not we are awaiting a mode to switch to.
     */
    bool is_awaiting = false;

    /**
     * Whether or not we have supercharged.
     */
    bool supercharged = false;

private:
    /**
     * Sets PWM on the MAV's pin.
     * @param dc The duty cycle
     */
    void mav_pwm(float dc);

    /**
     * Sets PWM on an SV's pin.
     * @param The valve to PWM (1-5)
     */
    void sv_pwm(int num);

    /**
     * Helper function to quickly set all the SV states at once.
     * @param A bitmask representing the 5 SV states to set
     */
    void set_sv_states(std::string mask);

    /**
     * Variables indicating certain conditions that affect valve states.
     */
    bool tanks_purging = false;
    bool engine_purging = false;
    bool filling = false;

    // TODO: Probably make handle a global variable
    int handle;

     /**
     * Pin assignments.
     */
    int sv_dio[5] = {SV1_DIO, SV2_DIO, SV3_DIO, SV4_DIO, SV5_DIO};
    int mav_dio = MAV_DIO;
};

#endif