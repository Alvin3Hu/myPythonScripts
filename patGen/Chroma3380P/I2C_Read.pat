                    *  11011  *TS2 , RPT 2   ;  //I2C Idle
                    *  10011  *TS2           ;  //I2C Start
                    *  10011  *TS1           ;
                    *  10011  *TS1           ;  //Device ID = 7'b0x3A
                    *  11011  *TS1           ;
                    *  11011  *TS1           ;
                    *  11011  *TS1           ;
                    *  10011  *TS1           ;
                    *  11011  *TS1           ;
                    *  10011  *TS1           ;
                    *  10011  *TS1           ;  //Access Type = 1'b0 Write
                    *  1L011  *TS1           ;  //ACK
                    *  1a011  *TS1           ;  //Reg Address MSB
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1a011  *TS1           ;
                    *  1L011  *TS1           ;  //ACK
                    *  10011  *TS2           ;  //I2C End
                    *  11011  *TS2 , RPT 2   ;  //I2C Idle
                    *  10011  *TS2           ;  //I2C Restart
                    *  10011  *TS1           ;
                    *  10011  *TS1           ;  //Device ID = 7'b0x3A
                    *  11011  *TS1           ;
                    *  11011  *TS1           ;
                    *  11011  *TS1           ;
                    *  10011  *TS1           ;
                    *  11011  *TS1           ;
                    *  10011  *TS1           ;
                    *  11011  *TS1           ;  //Access Type = 1'b1 Read
                    *  1L011  *TS1           ;  //ACK
                    *  1d011  *TS1           ;  //Reg Data Upper 8 Bits MSB
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  10011  *TS1           ;  //ACK
                    *  1d011  *TS1           ;  //Reg Data Lower 8 Bits MSB
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  1d011  *TS1           ;
                    *  11011  *TS1           ;  //ACK
                    *  10011  *TS2           ;  //I2C End
