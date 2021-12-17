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
        def __init__(self, num):
            pass
        def on(self):
            pass
        def off(self):
            pass

log = logging.getLogger("xmas-lights")

class AsyncLED:
    def __init__(self, num):
        self.num = num
        self.led = LED(num)

    async def on(self, sec):
        log.info("LED %d ON for %f sec", self.num, sec)
        self.led.on()
        await asyncio.sleep(sec)

    async def off(self, sec):
        log.info("LED %d OFF for %f sec", self.num, sec)
        self.led.off()
        await asyncio.sleep(sec)

m_sec = 60
h_sec = 60*60

async def run_led(num, schedule, rhyme):
    led = AsyncLED(num)

    while True:
        dt = datetime.datetime.now()
        h = dt.hour + dt.minute / m_sec + dt.second / h_sec
        flag = [flag for hour, flag in schedule if hour <= h][-1]

        if flag:
            if rhyme is not None:
                for on_sec, off_sec in rhyme:
                    await led.on(on_sec)
                    await led.off(off_sec)
            else:
                await led.on(m_sec)
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
        asyncio.create_task(run_led(17, schedule, None)),
        asyncio.create_task(run_led(22, schedule, random_rhyme)),
        asyncio.create_task(run_led(27, schedule, jingle_bells)),
        asyncio.create_task(randomise(schedule)),
    }

    await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)


if __name__ == "__main__":
    asyncio.run(main())
