from machine import Timer
from lora import send_data_to_app


class Clock:

    def __init__(self, handler, sleep):
        self.seconds = 0
        self.sleep=sleep
        self.handler = handler
        self.measurements = []
        self.__alarm = Timer.Alarm(self._seconds_handler, self.sleep, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += self.sleep
        print("%02d seconds have passed" % self.seconds)
        self.measurements.append(self.handler())
        if len(self.measurements) is 6:
            print(self.measurements)
            mean = self.measurements.pop(0)
            for i in range(len(self.measurements)):
                mean += self.measurements[i]
            mean = mean / 6
            self.measurements = []
            send_data_to_app(mean)
