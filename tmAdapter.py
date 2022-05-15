import string
from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys

class TMAdapter(Client):
    def __init__(self) -> None:
        super(TMAdapter, self).__init__()
        self.onUpdate = None

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time >= 0:
            state = iface.get_simulation_state()

            print(
                f'Time: {_time}\n' 
                f'Display Speed: {state.display_speed}\n'
                f'Position: {state.position}\n'
                f'Velocity: {state.velocity}\n'
                f'YPW: {state.yaw_pitch_roll}\n'
            )
            if self.onUpdate:
                self.onUpdate(state.yaw_pitch_roll)


    def attach(self, tmInterfaceNumber: string = ''):
        try:
            server_name = f'TMInterface{tmInterfaceNumber}' if tmInterfaceNumber != '' else 'TMInterface0'
            print(f'Connecting to {server_name}...')
            run_client(self, server_name)
        except AttributeError:
            print("AttributeError detected. Is the game running?")