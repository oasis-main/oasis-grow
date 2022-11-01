#---------------------------------------------------------------------------------------
#Manages Hardware for Heating
#---------------------------------------------------------------------------------------

#import shell modules
import sys
import signal

#set proper path for modules
sys.path.append('/home/pi/oasis-grow')

import rusty_pins
from peripherals import relays
from utils import concurrent_state as cs
from utils import error_handler as err

resource_name = "heater"
cs.check_lock(resource_name) #we check the lock here, because we are assigning a hardware resource on import

#get hardware config
cs.load_state()
heat_GPIO = int(cs.structs["hardware_config"]["equipment_gpio_map"]["heat_relay"]) #heater pin pulls from config file
pin = rusty_pins.GpioOut(heat_GPIO)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, cs.wrapped_sys_exit)
    try:
        while True:
            if cs.structs["feature_toggles"]["heat_pid"] == "1":
                print("Heating in pulse mode with " + cs.structs["control_params"]["heat_feedback"] + "%" + " power...")
                relays.actuate_slow_pwm(pin, float(cs.structs["control_params"]["heat_feedback"]), wattage=cs.structs["hardware_config"]["equipment_wattage"]["heater"], log="heater_kwh") #trigger appropriate response
            else:
                print("Heater on for " + cs.structs["control_params"]["heater_duration"] + " minute(s), off for " + cs.structs["control_params"]["heater_interval"] + " minute(s)...")
                relays.actuate_interval_sleep(pin, float(cs.structs["control_params"]["heater_duration"]), float(cs.structs["control_params"]["heater_interval"]), duration_units= "minutes", sleep_units="minutes", wattage=cs.structs["hardware_config"]["equipment_wattage"]["heater"], log="heater_kwh")
            cs.load_state()
    except SystemExit:
        print("Heater was terminated.")
    except KeyboardInterrupt:
        print("Heater was interrupted.")
    except Exception:    
        print("Heater encountered an error!")
        print(err.full_stack())
    finally:
        print("Shutting down heater...")
        try:
            relays.turn_off(pin)
        except:
            print(resource_name + " has no relay objects remaining.")
        
        cs.rusty_pipes.unlock(cs.lock_filepath, resource_name, 1000)
