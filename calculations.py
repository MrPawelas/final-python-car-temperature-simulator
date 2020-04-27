import time


class backend:
    def __init__(self, mass, surfaceOfCar, powerOfHeater, airTemp, desiredTemp, carTemp ):
        self.desiredTemp = desiredTemp
        self.carTemp = carTemp
        self.surfaceOfCar = surfaceOfCar
        self.powerOfHeater = powerOfHeater
        self.airTemp = airTemp
        self.mass = mass
        self.specificHeatAir = 1005  # kJ/kg⋅K
        self.thickness = 0.3  # meter thick
        # car parameters
        self.specificThermalConductivity = 50.2  # W/(m·K) steel
        self.efficiency = 0.6  # Energy conversion efficiency    #
        self.powerToHeat = powerOfHeater
        self.levelOfHeater = 50
        self.isStarted = 0  # 0 means that the start button wasn't clicked yet. 1 means that it just started so car's temperature will be the same as air, if it will be >1 it means that
        # that the button was clicked again and the car's temperature will adjust.
        self.allWorkOfHeater=0

        self.workInThisInterval=[]
        self.desiredTemperatures = []
        self.actualTemperatures = []
        self.times = []



    def heatConductedOverTime(self, deltaTime):
        Q = (self.specificThermalConductivity * (
                    self.airTemp - self.carTemp) * self.surfaceOfCar * deltaTime) / self.thickness
        return Q

    def deltaTemperatureAfterHeat(self, heat):
        return heat / (self.mass * self.specificHeatAir)

    def workOverTime(self,heatOrCool):
        return self.powerOfHeater * self.efficiency * (
                    self.levelOfHeater / 100) *heatOrCool # level of heater = 100 max cooling,  0 = cooling off


    def calculate(self, deltaTime):
        if self.mass==0:
            return
        Qair = self.heatConductedOverTime(deltaTime)
        Qheater=0
        heatOrCool =1 #heat=-1 cool=1
        if (self.carTemp < self.desiredTemp):
            heatOrCool=-1
        if (abs(self.carTemp - self.desiredTemp) > 0.5):
            self.levelOfHeater += 5
            self.levelOfHeater = min(self.levelOfHeater, 100)
            Qheater = self.workOverTime(heatOrCool)
        else:
            self.levelOfHeater =0
        self.allWorkOfHeater+=abs(Qheater)
        Q = Qair - Qheater

        deltaT = self.deltaTemperatureAfterHeat(Q)
        self.carTemp = self.carTemp + deltaT
        self.workInThisInterval.append(Qheater)

        return self.carTemp
