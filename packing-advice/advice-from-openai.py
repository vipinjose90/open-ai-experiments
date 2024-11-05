import os

from openai import OpenAI

openai_client = OpenAI()

# Predefined U-Haul truck dimensions (length x width x height in feet)
class Truck:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height


UHAUL_TRUCK_SIZES = {
    "10-foot": Truck(9.11, 6.4, 6.2),
    "15-foot": Truck(15, 7.8, 7.2),
    "20-foot": Truck(19.6, 7.8, 7.2),
    "26-foot": Truck(26.2, 8.5, 8.5)
}


class Box:
    def __init__(self, length, width, height, weight, fragile):
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
        self.weight = weight
        self.fragile = fragile


# Function to get truck dimensions based on the truck type
def get_truck_by_type(truck_type):
    if truck_type in UHAUL_TRUCK_SIZES:
        return UHAUL_TRUCK_SIZES[truck_type]
    else:
        print("Truck type not recognized. Please input dimensions manually.")
        return None


# Prompt user for box dimensions, weight, and fragility
def get_boxes():
    boxes = []
    while True:
        print("\nEnter box details:")
        length = float(input("Box length (in feet): "))
        width = float(input("Box width (in feet): "))
        height = float(input("Box height (in feet): "))
        weight = float(input("Box weight (in pounds): "))
        fragile = input("Is the box fragile? (yes/no): ").strip().lower() == 'yes'
        quantity = int(input("Quantity of this box type: "))

        box = Box(length, width, height, weight, fragile)
        boxes.extend([box] * quantity)  # Add multiple boxes of the same type

        more_boxes = input("Do you have more box types? (yes/no): ").strip().lower()
        if more_boxes != 'yes':
            break
    return boxes


# Function to communicate with ChatGPT for packing advice
def ask_chatgpt(question):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a packing assistant for U-Haul trucks."},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content
    return answer


# Generate a question for ChatGPT based on truck and box details
def get_loading_advice(truck, boxes):
    truck_info = f"Truck dimensions are {truck.length}x{truck.width}x{truck.height} feet with a volume of {truck.volume} cubic feet."
    box_details = ""
    for i, box in enumerate(boxes):
        fragility = "fragile" if box.fragile else "non-fragile"
        box_details += f"\nBox {i + 1}: {box.length}x{box.width}x{box.height} feet, {box.weight} lbs, {fragility}"

    question = f"""
    I have a U-Haul truck with {truck_info}. Here are my box details:{box_details}.
    How should I arrange these boxes for the best fit, considering weight, fragile items, and ensuring even weight distribution?
    """

    advice = ask_chatgpt(question)
    print("\nLoading Advice from ChatGPT:\n", advice)


def main():
    # Step 1: Get truck type from user and auto-fetch dimensions
    print("Choose your U-Haul truck type (e.g., 10-foot, 15-foot, 20-foot, 26-foot):")
    truck_type = input("Truck type: ").strip().lower()
    truck = get_truck_by_type(truck_type)

    if truck is None:
        return

    # Step 2: Input box dimensions, weight, and fragility
    boxes = get_boxes()

    # Step 3: Get loading advice from ChatGPT
    get_loading_advice(truck, boxes)

    # Optional Step 4: Allow user to add more boxes and get updated advice
    while input("\nAdd more boxes? (yes/no): ").strip().lower() == 'yes':
        new_boxes = get_boxes()
        boxes.extend(new_boxes)  # Add to existing list
        get_loading_advice(truck, boxes)  # Get updated advice from ChatGPT


if __name__ == "__main__":
    main()