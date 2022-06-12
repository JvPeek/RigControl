import string
from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
from rigControl import RigControl
import numpy as np

rollBuffer = []
rollBufferSize = 40
nextRollBufferIndex = 0

def normalizeRoll(roll: float):
    # global seems so wrong
    global rollBuffer 
    global rollBufferSize
    global nextRollBufferIndex
    
    if nextRollBufferIndex < len(rollBuffer) and len(rollBuffer) != 0: 
        rollBuffer[nextRollBufferIndex] = roll
    else:
        rollBuffer.append(roll)
    nextRollBufferIndex += 1

    if (nextRollBufferIndex >= rollBufferSize):
        nextRollBufferIndex = 0
    
    runningAverageRoll = 0
    for i in range(len(rollBuffer)): 
        runningAverageRoll += rollBuffer[i]
    
    runningAverageRoll /= rollBufferSize;
    print("Roll at normalizeRoll", runningAverageRoll)
    return runningAverageRoll

def capRoll(roll: float):
    # Cap the input at 90 Degrees
    if roll > 1: roll = 1
    if roll < -1: roll = -1
    print("Roll at capRoll", roll)
    return roll

def interpolateRoll(roll: float):
    roll = np.interp(roll, [-1, 1], [-35, 35])
    print("Roll at interpolateRoll", roll)
    return roll

def thresholdRoll(roll: float): 
    if roll < 1 and roll > -1: roll = 0
    print("Roll at thresholdRoll", roll)
    return roll

class TMAdapter(Client):
    def __init__(self, rigControl) -> None:
        super(TMAdapter, self).__init__()
        self.last_stepped_time = 0
        self.update_interval = 10
        self.rigControl = rigControl

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        self.rigControl.sendTurnToCommand(0, 2)

    def on_simulation_begin(self, iface: TMInterface):
        print(f'Started simulation {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time < 0:
            self.last_stepped_time = 0
            return 
        if (_time - self.last_stepped_time) < self.update_interval:
            return

        print("##### BEGIN ######")
        state = iface.get_simulation_state()
        roll = state.yaw_pitch_roll[2]
        roll = normalizeRoll(roll)
        roll = capRoll(roll)
        roll = interpolateRoll(roll)
        roll = thresholdRoll(roll)

        roll = roll * -1

        print(
            f'Time: {_time}\n' 
            f'Roll: {roll}\n'
        )

        self.rigControl.sendTurnToCommand(roll, 15)
        self.last_stepped_time = _time

        print("##### END ######\n\n\n\n")
        

        

    def attach(self, tmInterfaceNumber: string = ''):
        try:
            server_name = f'TMInterface{tmInterfaceNumber}' if tmInterfaceNumber != '' else 'TMInterface0'
            print(f'Connecting to {server_name}...')
            run_client(self, server_name)
        except AttributeError:
            print("AttributeError detected. Is the game running?")