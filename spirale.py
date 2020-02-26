# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 09:10:53 2019

@author: Rishad
"""
""" 
A Class definition for the Spirale3 Environmental Chamber.
Feel free to make modifications as required.

""" 
import telnetlib

class spirale3:
    
        
    def __init__(self, HOST='10.8.88.121', PORT='888'):
        """Initialise chamber IP and Port"""

        # Environmental Chamber Static Assigned IP
        self.HOST= HOST
        # Environmental Chamber Telnet Port                                 
        self.PORT= PORT           
    
    def initChamber(self, profile = 'Manual-Mode'):
        """ Set the chamber profile.
        
        The default setting selects Manual-Mode which allows you to change the 
        temperature settings over the network. 
        
        You can call this method and enter the name of a profile stored on the 
        chamber's local memory as an argument.
        The chamber will then automatically switch to
        the stored profile.
        
        eg.
        
        mychamber = spirale3()
        mychamber.initChamber("Noise diode stability")

        """

        try:
            # Create telnet session
            self.session = telnetlib.Telnet(self.HOST,self.PORT)
            self.setProfile = 'Programme en cours = "{}"\r\n'.format(profile)
            # Write Profile to chamber
            self.session.write(bytes(self.setProfile,'utf-8'))
            # Read response from chamber
            session_read = self.session.read_until(b'\r\n')
            
            if session_read.decode('utf-8') == self.setProfile:
                print("Chamber profile set to: "+ profile)
            else:
                print("Error! Could not set Chamber profile.")
            #Send the command to read the programme           
            self.session.write(b'?Programme en cours\r\n')
            #Read the data from the Temp Chamber until the end char is received           
            chamber_profile = self.session.read_until(b'\r\n')
            # Close telnet session
            self.session.close()    
            print(chamber_profile.decode('utf-8'))

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)
                        
        except Exception as e:
            print(e)
            
    def startChamber(self):
        """
        Starts the chamber

        Returns string with confirmation message from chamber

        """

        try:
            print('Turning on Environmental Chamber....\n')
            # Create telnet session
            self.session = telnetlib.Telnet(self.HOST,self.PORT)
            # start chamber
            self.session.write(b'Marche_arret=1\r\n')
            session_read = self.session.read_until(b'\r\n')
            
            if session_read == (b'Marche_arret=1\r\n'):
                print('Environmental Test Started.')
            else:
                 print('Error! Could not start Environmental Test')
            self.session.close()
            return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)
            
    def stopChamber(self):
        """
        Stops the chamber.

        Returns string with confirmation message from chamber
        """

        try:
            print('Turning off Environmental Chamber....\n')
            self.session = telnetlib.Telnet(self.HOST,self.PORT)            
            self.session.write(b'Marche_arret=0\r\n')
            session_read = self.session.read_until(b'\r\n')
            
            if session_read == (b'Marche_arret=0\r\n'):
                print('Environmental test successfully stopped.')
            else:
                print('Error! Could not stop environmental test.')
            self.session.close()    
            return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)
    
    def cancelTest(self,save):
        """
        End the test.

        You can choose whether to save the test records to memory or not by
        passing an integer 1 or 0 when calling cancelTest().
        
        eg.
        - To end test and save the test records to the chamber's local memory:
            
        mychamber.cancelTest(1)
        
        eg.
        - To end test without saving the test records to the chamber's local 
        memory:

        mychamber.cancelTest(0)

        Returns string with confirmation message from chamber
        
        """

        try:
            if save == 1:
                print('Cancelling test and saving test records...')
                self.session = telnetlib.Telnet(self.HOST,self.PORT)
                self.session.write(b'Annulation_essai=1\r\n')
                session_read = self.session.read_until(b'\r\n')
                self.session.close()
                return session_read
            else:
                print('Cancelling test without saving test records...')
                self.session = telnetlib.Telnet(self.HOST,self.PORT)
                self.session.write(b'Annulation_essai=0\r\n')
                session_read = self.session.read_until(b'\r\n')
                self.session.close()
                return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)
            
        except Exception as e:
            print(e)
        
    
    def getTemperature(self):
        """
        Gets the current chamber temperature.

        Returns the current temperature as a floating point number
        """

        try:
            self.session = telnetlib.Telnet(self.HOST,self.PORT)
            #Send the command to read the current temperature
            self.session.write(b'?tcuve\r\n')
            #Read the data from the Temp Chamber until the end char is received                       
            self.chamber_temp = self.session.read_until(b'\r\n')
            #Close telnet session
            temperature = self.chamber_temp.decode('UTF-8')
            #Only keep the the temperature data     
            temperature = temperature[temperature.find('=')+1:temperature.find('\r')-1]
            self.session.close()
            return float(temperature)

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)
    
    def setTemperature(self, setPoint,period):
        """
        Set temperature.

        Arguments:

        setPoint - temperature in degrees celcius.
        period - time period in seconds.

        eg, Set the chamber to ramp to 25 degrees over 5 minutes.

        5 minutes = 300 seconds.

        mychamber.setTemperature(25,300)

        Returns string with confirmation message from chamber
        """

        try:
            self.setPoint = str(setPoint)+'>'+str(period)
            print('Setting Environmental Chamber to: '+self.setPoint)
            setTemp = 'conscuve = '+self.setPoint+'\r\n'
            self.session = telnetlib.Telnet(self.HOST,self.PORT)
            self.session.write(bytes(setTemp,'utf-8'))
            session_read = self.session.read_until(b'\r\n')
            
            if session_read.decode('utf-8') == setTemp:
                print("Temperature setpoint is set to "+str(setPoint)+" degrees celcius over a period of "+str(period)+" seconds.")
            else:
                print("Error! Could not set temperature setpoint.")
            self.session.close()    
            return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)

    def getHumidity(self):
        """
        Function that gets the humidity of the chamber. Usage is similar to getTemperature.

        Returns humidity value as a floating point number.
        
        """
        try:
            print('Getting current humidity of Environmental Chamber....')
            self.session = telnetlib.Telnet(self.HOST,self.PORT)                 
            #Send the command to read the current humidity
            self.session.write(b'?humcuve\r\n')
            #Read the data from the Temp Chamber until the end char is received                       
            self.chamber_hum = self.session.read_until(b'\r\n')
            humidity = self.chamber_hum.decode('UTF-8')
            #Only keep the the humidity data     
            humidity = humidity[humidity.find('=')+1:humidity.find('\r')-1]  
            self.session.close()
            return humidity

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)
    
    def setHumidity(self, setPoint,period):
        """
        Function that sets the Humidity of the chamber for a specific period of time.

        - Usage

        - setPoint : Humidity in percent
        - period : time period in seconds.

        Usage is similar to setTemperature.

        Returns string with confirmation message from chamber
        """
        try:
            self.setPoint = str(setPoint)+'>'+str(period)
            print('Setting Environmental Chamber to: '+self.setPoint)
            self.session = telnetlib.Telnet(self.HOST,self.PORT)
            setHum = 'conshum = '+self.setPoint+'\r\n'
            self.session.write(bytes(setHum,'utf-8'))
            session_read = self.session.read_until(b'\r\n')
            self.session.close()
            return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)
        
        except Exception as e:
            print(e)

    def pauseCycle(self,pause):
        """
        Pause/Resume current temperature cycle.
        
        eg.
        - To pause test:
            
        mychamber.pauseCycle(1)
        
        eg.
        - To resume test:
        
        mychamber.pauseCycle(0)

        Returns string with confirmation message from chamber
        
        
        """
        try:
            if pause == 1:
                self.session = telnetlib.Telnet(self.HOST,self.PORT)
                self.session.write(b'PauseProg=1\r\n')
                session_read = self.session.read_until(b'\r\n')
                if session_read == (b'PauseProg=1\r\n'):
                    print('Cycle Paused.')
                else:
                    print('Error! Could not pause cycle.')
                self.session.close()
                return session_read
            else:
                self.session = telnetlib.Telnet(self.HOST,self.PORT)
                self.session.write(b'PauseProg=0\r\n')
                session_read = self.session.read_until(b'\r\n')
                if session_read == (b'PauseProg=0\r\n'):
                    print('Cycle Resume.')
                else:
                    print('Error! Could not resume cycle.')                
                self.session.close()
                return session_read

        except IOError as socket_error:
            print("Connection could not be established. Check IP address or physical connection")
            print(socket_error)

        except Exception as e:
            print(e)