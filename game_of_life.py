from cuesdk import CueSdk
from cuesdk import CorsairLedId
import threading
import queue
import time
from keyboard import Keyboard


def read_keys(inputQueue):
    while (True):
        input_str = input()
        inputQueue.put(input_str)

def life_happens(keyboard: Keyboard):
    """The rules of the game of life are followed to move forward one step.
    
    If a cell is ON and has fewer than two neighbors that are ON, it turns OFF
    If a cell is ON and has either two or three neighbors that are ON, it remains ON.
    If a cell is ON and has more than three neighbors that are ON, it turns OFF.
    If a cell is OFF and has exactly three neighbors that are ON, it turns ON.
    """
    on_color = (255, 0, 0)
    off_color = (0, 0, 0)
    for key in keyboard._keyboard:
        neighbors = keyboard.get_key_neighbors(key)
        neighbors_on = keyboard.num_match_color(neighbors, on_color)

        # 1
        if keyboard.get_key_color(key) == on_color:
            keyboard.set_key_buffer(key, on_color)
            if neighbors_on < 2:
                keyboard.set_key_buffer(key, off_color)
        
        # 3
            elif neighbors_on > 4:
                keyboard.set_key_buffer(key, off_color)
        
        # 4
        else:
            if neighbors_on == 3 or neighbors_on == 4:
                keyboard.set_key_buffer(key, on_color)

        
    
    keyboard.set_led_colors_flush_buffer()


def main():
    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_keys,
                                   args=(inputQueue, ),
                                   daemon=True)
    inputThread.start()
    
    keyboard = Keyboard()
    keyboard.set_layer_priority(126)

    print("Working... Use \"+\" or \"-\" to increase or decrease speed.\n" +
          "Press \"q\" to close program...")
    while (True):
        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get()

            if input_str == "q" or input_str == "Q":
                print("Exiting.")
                break

        #keyboard.set_key(CorsairLedId.K_G, (255, 0, 0))

        life_happens(keyboard)

        time.sleep(.5)


if __name__ == "__main__":
    main()