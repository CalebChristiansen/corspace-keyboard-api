"""Contains the keyboard class."""
from typing import Sequence
from cuesdk import CueSdk
from cuesdk.helpers import ColorRgb
from cuesdk import CorsairLedId

_KEYBOARD_INDEX = 0

class Keyboard(CueSdk):
    """A representation of the keyboard.
    
    Class Variables:
        _keyboard (dict): A dictionary of all the keys (key represented as `cuesdk.CorsairLedId`)
            and their coresponding grid positions (position represented as a tuple).
            This argument can be grabbed from the cuesdk by using commands:
            `sdk = CueSdk()`
            `device_index = sdk.get_device_count()[0]`
            `led_positions = sdk.get_led_positions_by_device_index(device_index)`
    """

    def __init__(self):
        super().__init__()

        connected = self.connect()
        if not connected:
            err = self.get_last_error()
            print("Handshake failed: %s" % err)
        
        try:
            self._keyboard = self.get_led_positions_by_device_index(_KEYBOARD_INDEX)
        except:
            print("unable to load/find keyboard")
    
    def set_key(self, key_id: CorsairLedId, color):
        """Sets the color of a key and pushes buffer.

        Args:
            key_id (CorsairLedId): the key to change
            color (sequence): the color (255, 255, 255) to change the key to.
        """
        self.set_key_buffer(key_id, color)
        self.set_led_colors_flush_buffer()
    
    def set_key_buffer(self, key_id: CorsairLedId, color):
        """Sets the color of a key in buffer.

        Args:
            key_id (CorsairLedId): the key to change
            color (sequence): the color (255, 255, 255) to change the key to.
        """
        key_to_change = {
            key_id: color,
        }
        self.set_led_colors_buffer_by_device_index(_KEYBOARD_INDEX, key_to_change)
    
    def get_key_color(self, key_id: CorsairLedId):
        """returns a (r, g, b) tuble representing key color."""
        dictionary = self.get_led_colors_by_device_index(_KEYBOARD_INDEX, (key_id,))
        return dictionary[key_id]

    def get_key_colors(self, key_ids: list):
        """returns a dict of key colors."""
        return self.get_led_colors_by_device_index(_KEYBOARD_INDEX, key_ids)

    def get_key_neighbors(self, key_id: CorsairLedId, distance = 35) -> list:
        """returns a list of keys that neighbor this key."""
        neighbors = []
        for neighbor_id in self._keyboard:
            neighbor_distance = self.get_keys_separation(key_id, neighbor_id)
            if (neighbor_distance < distance) and (neighbor_id != key_id):
                neighbors.append(neighbor_id)
        return neighbors
    
    def get_keys_separation(self, key_a: CorsairLedId, key_b: CorsairLedId) -> float:
        """returns the distance between two keys using pythag theorem."""
        location_a = self._keyboard[key_a]
        location_b = self._keyboard[key_b]
        locations = zip(location_a, location_b)
        return sum( [(list_a_i - list_b_i)**2 for list_a_i, list_b_i in locations] )**(1/2)
    
    def num_match_color(self, keys: Sequence[CorsairLedId], color: Sequence[int]):
        """returns the number of keys in sequence that match the color"""
        matches: int = 0
        for key in keys:
            if self.get_key_color(key) == color:
                matches += 1
        return matches
