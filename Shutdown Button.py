#!/usr/bin/env python3
from gpiozero import Button, PWMLED
import pygame.mixer
from signal import pause
import time
import os, sys

##Our variables
shutdownSound = "WindowsXP_Shutdown_Sound.mp3"
startupSound =  "Windows95_Startup_sound.mp3"
shutdownMode = False
fadeRate = 0.50 
blinkRate = 0.15
shutdownFadeRate = 0.05
holdTime = 5 #hold time until shutdown

##GPIO pins used
buttonGPIO = 3 #Button to GPIO 3
ledGPIO = 21 #LED to GPIO 21

##Our important functions
def when_pressed():
    # Fade Led to notify the system is On
    whiteLED.pulse(fadeRate,fadeRate,None,True) #fade an LED in background on a hald second interval
             
def when_held():    
    global shutdownMode
    
    shutdownMode=True
    # start blinking rapidly
    whiteLED.blink(blinkRate, blinkRate,0,0, None, True)
    
def when_released():
    global shutdownMode
    
    if(shutdownMode):
        #Shutdown the Raspberry Pi
        whiteLED.pulse(shutdownFadeRate,shutdownFadeRate,None,True)
        shutdownMode = False
        shutdown()
    else:
        #User didn't mean to shutdown
        whiteLED.on()
        
def shutdown():
    playSoundFile(shutdownSound)
    while (pygame.mixer.music.get_busy()):  #Wait till our song finishes, then shutdown
        continue
    #print("Shutting Down...")
    os.system("sudo poweroff")
    
def playSoundFile(soundFile):
    pygame.mixer.music.load(sys.path[0]+"/"+ soundFile) #we need to load the music file's absolute location, since the terminal doesn't use Shell
    if(soundFile == startupSound):
        setVolume(0.61) #the startup sound has a little static, so we'll decrease the volume
    else:
        setVolume(1.0) #Set the volume a little more louder for shutdown sound
    pygame.mixer.music.play()
def setVolume(volumeLevel):
    pygame.mixer.music.set_volume(volumeLevel)


########Setup up our GPIO Pins
whiteLED = PWMLED(ledGPIO)
btn = Button(buttonGPIO, hold_time = holdTime)

#########This happens at Startup
pygame.init()
playSoundFile(startupSound)
while (pygame.mixer.music.get_busy()):  #Wait till our song finishes, then shutdown
        whiteLED.on() #For some reason, the led doesn't turn on the first time. So putting it in a loop will eventually trigger it
        continue
btn.when_held = when_held
btn.when_pressed = when_pressed
btn.when_released = when_released

pause()  #This is much better than using an infinite loop
         #and constantly checking if buttons were pressed;
         #it doesn't drain any CPU, so that's good.
#########


