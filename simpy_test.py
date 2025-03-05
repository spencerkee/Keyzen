import simpy_keyboard

def typing_process(env, text, distance_matrix, time_per_distance):
    """
    Simulates the process of typing a given text with two fingers.

    Args:
        env: SimPy environment.
        text: The string to be typed.
        distance_matrix: A dictionary of dictionaries representing distances between characters.
                         distance_matrix[char1][char2] gives the distance from char1 to char2.
        time_per_distance: Constant time taken to travel a unit distance.
    """

    left_hand_chars = set("qwerasdfzxcv")
    right_hand_chars = set("yuiophjklbnm")

    last_char_left = None  # Keep track of the last character typed by the left hand
    last_char_right = None # Keep track of the last character typed by the right hand

    print(f"Start typing '{text}' at time {env.now}")

    for char in text.lower(): # Convert to lowercase for easier handling

        if char not in distance_matrix:
            print(f"Warning: Character '{char}' not found in distance matrix. Assuming 0 travel time.")
            typing_time = 0.0
        else:
            typing_time = 0.0 # Initialize typing time for this character

            if char == ' ': # Space can be pressed by either hand, or both in quick succession. Let's simplify and say last hand presses it.
                if last_char_left is not None and last_char_left in distance_matrix and ' ' in distance_matrix[last_char_left]:
                    typing_time_left = distance_matrix[last_char_left][' '] * time_per_distance
                else:
                    typing_time_left = 0.0

                if last_char_right is not None and last_char_right in distance_matrix and ' ' in distance_matrix[last_char_right]:
                    typing_time_right = distance_matrix[last_char_right][' '] * time_per_distance
                else:
                    typing_time_right = 0.0

                # Take the minimum time if both hands could have pressed space quickly from their last positions
                if last_char_left is not None and last_char_right is not None:
                    typing_time = min(typing_time_left, typing_time_right)
                elif last_char_left is not None:
                    typing_time = typing_time_left
                elif last_char_right is not None:
                    typing_time = typing_time_right
                else:
                    typing_time = 0.0  # First char is space?

                last_hand = "both" # For space, we can consider it as 'both' or simply update both last_chars


            elif char in left_hand_chars:
                if last_char_left is not None and last_char_left in distance_matrix and char in distance_matrix[last_char_left]:
                    typing_time = distance_matrix[last_char_left][char] * time_per_distance
                else:
                    typing_time = 0.0  # No travel if it's the first left hand char or no distance known
                last_char_left = char
                last_char_right = last_char_right # Right hand remains unchanged

            elif char in right_hand_chars:
                if last_char_right is not None and last_char_right in distance_matrix and char in distance_matrix[last_char_right]:
                    typing_time = distance_matrix[last_char_right][char] * time_per_distance
                else:
                    typing_time = 0.0 # No travel if it's the first right hand char or no distance known
                last_char_right = char
                last_char_left = last_char_left # Left hand remains unchanged
            else:
                print(f"Warning: Character '{char}' is not assigned to any hand. Assuming 0 travel time.")
                typing_time = 0.0

        if typing_time > 0:
            yield env.timeout(typing_time) # Wait for the typing time
            print(f"Typed '{char}' at time {env.now} (took {typing_time:.3f})")
        else:
            print(f"Typed '{char}' at time {env.now} (took {typing_time:.3f}) - No travel time")


    print(f"Finished typing '{text}' at time {env.now}")


# Example Usage:

# 1. Define a sample distance matrix (replace with your actual matrix)
#    This is a simplified example. Real distances would need to be calculated/measured.
distance_matrix = {
    'q': {'w': 1, 'a': 1, ' ': 2},
    'w': {'e': 1, 's': 1, 'q': 1, ' ': 2},
    'e': {'r': 1, 'd': 1, 'w': 1, ' ': 2},
    'r': {'t': 1, 'f': 1, 'e': 1, ' ': 2},
    't': {'y': 1, 'g': 1, 'r': 1, ' ': 2},
    'y': {'u': 1, 'h': 1, 't': 1, ' ': 2},
    'u': {'i': 1, 'j': 1, 'y': 1, ' ': 2},
    'i': {'o': 1, 'k': 1, 'u': 1, ' ': 2},
    'o': {'p': 1, 'l': 1, 'i': 1, ' ': 2},
    'p': {';': 1, 'o': 1, ' ': 2}, # Assuming ';' is next to p, adjust if needed
    'a': {'s': 1, 'q': 1, 'z': 1, ' ': 2},
    's': {'d': 1, 'w': 1, 'a': 1, 'x': 1, ' ': 2},
    'd': {'f': 1, 'e': 1, 's': 1, 'c': 1, ' ': 2},
    'f': {'g': 1, 'r': 1, 'd': 1, 'v': 1, ' ': 2},
    'g': {'h': 1, 't': 1, 'f': 1, 'b': 1, ' ': 2},
    'h': {'j': 1, 'y': 1, 'g': 1, 'n': 1, ' ': 2},
    'j': {'k': 1, 'u': 1, 'h': 1, 'm': 1, ' ': 2},
    'k': {'l': 1, 'i': 1, 'j': 1, ',': 1, ' ': 2}, # Assuming ',' is next to k, adjust if needed
    'l': {';': 1, 'o': 1, 'k': 1, '.': 1, ' ': 2}, # Assuming '.' is next to l, adjust if needed
    ';': {'p': 1, 'l': 1, '/': 1, ' ': 2}, # Assuming '/' is next to ';', adjust if needed
    'z': {'x': 1, 'a': 1, ' ': 2},
    'x': {'c': 1, 's': 1, 'z': 1, ' ': 2},
    'c': {'v': 1, 'd': 1, 'x': 1, ' ': 2},
    'v': {'b': 1, 'f': 1, 'c': 1, ' ': 2},
    'b': {'n': 1, 'g': 1, 'v': 1, ' ': 2},
    'n': {'m': 1, 'h': 1, 'b': 1, ' ': 2},
    'm': {',': 1, 'j': 1, 'n': 1, ' ': 2},
    ',': {'k': 1, 'm': 1, '.': 1, ' ': 2},
    '.': {'l': 1, ',': 1, '/': 1, ' ': 2},
    '/': {';': 1, '.': 1, ' ': 2},
    ' ': {'q': 2, 'w': 2, 'e': 2, 'r': 2, 't': 2, 'y': 2, 'u': 2, 'i': 2, 'o': 2, 'p': 2,
          'a': 2, 's': 2, 'd': 2, 'f': 2, 'g': 2, 'h': 2, 'j': 2, 'k': 2, 'l': 2, ';': 2,
          'z': 2, 'x': 2, 'c': 2, 'v': 2, 'b': 2, 'n': 2, 'm': 2, ',': 2, '.': 2, '/': 2} # Example distances from space
}

# Make sure the distance matrix is symmetric if it should be in your case.
# If distance from 'a' to 'b' is X, distance from 'b' to 'a' should also be X (typically).
for char1 in list(distance_matrix.keys()): # Iterate over a copy to allow modification
    for char2 in list(distance_matrix[char1].keys()):
        if char2 not in distance_matrix:
            distance_matrix[char2] = {}
        if char1 not in distance_matrix[char2]:
            distance_matrix[char2][char1] = distance_matrix[char1][char2]


# 2. Set the time per distance unit
time_per_distance_unit = 0.1  # e.g., 0.1 seconds per unit distance

# 3. Input text to type
text_to_type = "The quick brown fox"

# 4. Create SimPy environment and run the simulation
env = simpy_keyboard.Environment()
env.process(typing_process(env, text_to_type, distance_matrix, time_per_distance_unit))
env.run()