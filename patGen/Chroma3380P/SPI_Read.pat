                    *  100X111  *TS1           ;  //SPI Idle
                    *  100X111  *RPT 2         ;
                    *  000X111  *TS1           ;  //SPI Start
                    *  010X111  *TS1           ;  //Device ID = 7'b0x3A
                    *  011X111  *TS1           ;
                    *  011X111  *TS1           ;
                    *  011X111  *TS1           ;
                    *  010X111  *TS1           ;
                    *  011X111  *TS1           ;
                    *  010X111  *TS1           ;
                    *  011X111  *TS1           ;  //Access Type = 1'b1 Read
                    *  01aX111  *TS1           ;  //Reg Address MSB
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  01aX111  *TS1           ;
                    *  010d111  *TS1           ;  //Reg Data MSB
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  010d111  *TS1           ;
                    *  100X111  *TS1           ;  //SPI End
