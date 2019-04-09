from machine import Timer


class Clock:

    def __init__(self, handler,sleep):
        self.seconds = 0
        self.sleep=sleep
        self.handler = handler
        self.__alarm = Timer.Alarm(self._seconds_handler, self.sleep, periodic=True)

    def _seconds_handler(self, alarm):
        self.seconds += self.sleep
        print("%02d seconds have passed" % self.seconds)
        self.handler()

        if self.seconds > 30:
            alarm.callback(None) # stop counting after 30 seconds
