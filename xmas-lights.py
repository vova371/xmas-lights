#!/usr/bin/env python3

import os
import asyncio
import numpy as np
import datetime
import logging

try:
    from gpiozero import LED
except ImportError:
    print("gpiozero module not available, using dummy LED implementation")

    class LED:
        def __init__(self, pin):
            self.pin = pin
            self.value = 0

        def on(self):
            self.value = 1

        def off(self):
            self.value = 0

        def toggle(self):
            self.value = 0 if self.value else 0

        @property
        def is_lit(self):
            return bool(self.value)

log = logging.getLogger("xmas-lights")

class AsyncLED:
    def __init__(self, pin):
        self.led = LED(pin)

    async def on(self, sec):
        log.info("LED %d ON for %f sec", self.led.pin, sec)
        self.led.on()
        await asyncio.sleep(sec)

    async def off(self, sec):
        log.info("LED %d OFF for %f sec", self.led.pin, sec)
        self.led.off()
        await asyncio.sleep(sec)


class CounterPhasePair:
    def __init__(self, a, b):
        self.led_a = LED(a)
        self.led_b = LED(b)

    async def on_a(self, sec):
        log.info("LED %d ON, %d OFF for %f sec", self.led_a.pin, self.led_b.pin, sec)
        self.led_a.on()
        self.led_b.off()
        await asyncio.sleep(sec)

    async def on_b(self, sec):
        log.info("LED %d ON, %d OFF for %f sec", self.led_b.pin, self.led_a.pin, sec)
        self.led_a.off()
        self.led_b.on()
        await asyncio.sleep(sec)

    async def off(self, sec):
        log.info("LED %d OFF, %d OFF for %f sec", self.led_a.pin, self.led_b.pin, sec)
        self.led_a.off()
        self.led_b.off()
        await asyncio.sleep(sec)


m_sec = 60
h_sec = 60*60

def check_schedule(schedule):
    dt = datetime.datetime.now()
    h = dt.hour + dt.minute / m_sec + dt.second / h_sec
    return [flag for hour, flag in schedule if hour <= h][-1]

async def scheduled_light(pin, schedule):
    led = AsyncLED(pin)

    while True:
        if check_schedule(schedule):
            await led.on(m_sec)
        else:
            await led.off(m_sec)

async def scheduled_rhyme(pin, schedule, rhyme):
    led = AsyncLED(pin)

    while True:
        if check_schedule(schedule):
            for on_sec, off_sec in rhyme:
                await led.on(on_sec)
                await led.off(off_sec)
        else:
            await led.off(m_sec)


async def counter_phase_pair(a, b, schedule, rhyme):
    led = CounterPhasePair(a, b)

    while True:
        if check_schedule(schedule):
            for a_sec, b_sec in rhyme:
                await led.on_a(a_sec)
                await led.on_b(b_sec)
        else:
            await led.off(m_sec)


async def randomise(schedule):
    orig = np.array([rule[0] for rule in schedule[1:]])

    while True:
        shifted = orig + np.random.rand(len(orig)) * 0.5 - 0.25  # +/- 15 min
        for i in range(len(orig)):
            schedule[i+1][0] = shifted[i]
        log.info("randomised schedule: %s", schedule)
        await asyncio.sleep(h_sec * 24)

async def main():
    logging.basicConfig(
        filename=os.path.splitext(__file__)[0] + ".log",
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )

    # 00:00 - Lights On
    # 01:00 - Lights Off
    # 15:00 - Lights On
    schedule = [[0, True], [1, False], [15, True]]
    log.info("starting with schedule: %s", schedule)

    sz = 1000
    a = np.exp(np.random.rand(sz) * 2.5 - 1)
    b = np.exp(np.random.rand(sz) * 2.5 - 1.5)
    random_rhyme = np.reshape(np.dstack((a,b)), (sz, 2))

    jingle_bells = [
        (0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
        (0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
        (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
        (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.75, 0.25),
        (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.25, 0.25), (0.75, 2.25),
    ]

    tasks = {
        asyncio.create_task(randomise(schedule)),
        asyncio.create_task(scheduled_light(17, schedule)),
        asyncio.create_task(counter_phase_pair(22, 27, schedule, random_rhyme)),
    }

    await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)


if __name__ == "__main__":
    asyncio.run(main())
