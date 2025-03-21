'''import board
import digitalio
import storage

rw_toggle = digitalio.DigitalInOut(board.GP28)
rw_toggle.direction = digitalio.Direction.INPUT
rw_toggle.pull = digitalio.Pull.UP

# If the GP28 is connected to ground with a wire
# CircuitPython can write to the drive
storage.remount("/", readonly=rw_toggle.value)'''