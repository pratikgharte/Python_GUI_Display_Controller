from AtlasOEM_PH import AtlasOEM_PH
import time

def main(): 
    PH = AtlasOEM_PH() # create an OEM PH object

    PH.write_active_hibernate(1) # tell the circuit to start taking readings

    
    if PH.read_new_reading_available():              # if we have a new reading
            pH_reading = PH.read_PH_reading()            # get it from the circuit
            print("OEM pH reading: " + str(pH_reading))  # print the reading
            PH.write_new_reading_available(0)   # then clear the new reading register 
                                                # so the circuit can set the register
                                                # high again when it acquires a new reading
            
            PH.read_calibration_data()
            pH_CalData = PH.read_calibration_data()
                #return self.read_32(0x08)/1000.0
            print("OEM pH CAL reading: " + str(pH_CalData))
            PH.write_calibration_data1(0X00)
            PH.write_calibration_data2(0X00)
            PH.write_calibration_data3(0X27)
            PH.write_calibration_data4(0X10)
            PH.write_calibration_request(3)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
            time.sleep(5)
            #PH.write_calibration_request(2)
            pH_ReadCal = PH.read_calibration_confirm()
            print("OEM pH CALCONF reading: " + str(pH_ReadCal))
            
            
                                
        
if __name__ == '__main__':
    main()

