import appdaemon.plugins.hass.hassapi as hass
import ha_version

class Get_Shit(hass.Hass): # Deklarerer egenskaper for klassen.

   def initialize(self):
        self.log(
            f"🚨 Launching VegvesenScraper {ha_version.__version__}",
            ascii_encode=False,
        )
        self.load_sensors()
        runtime = datetime.time(0, 0, 0)
        self.run_hourly(self.run_hourly_callback, runtime)          # Kjører automatisk. Skal endre til å kjøres hvert 5.minutt
  
   def run_hourly_callback(self, kwargs):
        self.getData()
        try:
            self.postSensor()
        except:
            self.log("Something went terribly wrong.")
            pass



    def load_sensors(self): #Kjører ved oppstart
        



#       self.set_state("sensor.postpakker",
#           state=str(self.total_pakker) + (" pakke på vei" if self.total_pakker == 1 else " pakker på vei"),
#           replace = True, attributes= {
#           "icon": "mdi:mail",
#           "friendly_name": "postsporer",
#           "Info": self.data
#        })
