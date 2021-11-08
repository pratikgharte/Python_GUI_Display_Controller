from AtlasOEM_EC import AtlasOEM_EC
import time

def main(): 
    EC = AtlasOEM_EC # create an OEM PH object

    EC.write_active_hibernate(1) # tell the circuit to start taking readings   
    EC.read_calibration_data()
    EC_CalData = EC.read_calibration_data()
                #return self.read_32(0x08)/1000.0
    print("OEM EC CAL reading: " + str(EC_CalData))
    EC.write_calibration_data1(0X00)
    EC.write_calibration_data2(0X00)
    EC.write_calibration_data3(0X1B)
    EC.write_calibration_data4(0X5A)
    EC.write_calibration_request(2)
            #PH.write_calibration_request(2)
            #PH.write_calibration_request(0)
            #PH.read_calibration_confirm()
            #time.sleep(1)
    time.sleep(20)
            #PH.write_calibration_request(2)
    EC_ReadCal = PH.read_calibration_confirm()
     print("OEM pH CALCONF reading: " + str(EC_ReadCal))
            
            
                                
        
if __name__ == '__main__':
    main()

