import json
import time
import os
import sys
import asyncio
import concurrent.futures
import json
import os
import time
import pygame
from PushUpCounter import PushUpCounter

pygame.mixer.init()

async def alarm_sequence(id):
    # Read JSON file for settings
    with open("alarms.json") as json_file:
        data = json.load(json_file)

    extreme_mode = data[str(id)]["extreme"]  # number of pushups or squats
    alarm_sound = data[str(id)]["music"]
    # Play alarm sound
    if alarm_sound!=None:
        print("Playing alarm sound")
        song = pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play()
        
    # Start pushup counter and wait for it to finish
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, lambda: PushUpCounter.start_pushup_counter(extreme_mode))
        print(result)

    # Stop light strobe after pushup counter finishes

    # Stop alarm sound
    if alarm_sound!=None:
        song.stop()


playing = False

while True:
    with open('alarms.json') as json_file:
        data = json.load(json_file)
    
    numAlarms = data["numberOfAlarms"]
    for i in range(numAlarms):
        if data[str(i)]["active"]:
            if data[str(i)]["time"] == time.strftime("%H:%M"):
                print("Alarm!")
                if not playing:
                    playing = True
                    asyncio.run(alarm_sequence(i))
            
            else:
                playing = False

    time.sleep(1)


