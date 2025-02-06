import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os
from datetime import datetime

def letter_to_number(letter):
    """Convert a letter to a numeric value (A=1, ..., Z=26)."""
    value = ord(letter.upper()) - ord('A') + 1
    return value

def name_to_numbers(name):
    """Convert a name to a list of numeric values based on letters."""
    return [letter_to_number(char) for char in name if char.isalpha()]

def generate_fractal(name_numbers, size=500, iterations=100):
    """Generate a unique fractal image based on numeric values."""
    if not name_numbers:
        name_numbers = [1]  # Default in case of empty input

    # Dynamic parameters based on the name's numeric values
    scale_x = sum(name_numbers) % 10 + 1
    scale_y = (sum(name_numbers[::-1]) % 10 + 1) * 1.5
    c_real = sum(name_numbers[::2]) / len(name_numbers)
    c_imag = sum(name_numbers[1::2]) / len(name_numbers)

    # Introduce more variability in the fractal formula
    noise_factor = (sum(name_numbers) % 5) / 100  # Small noise factor
    extra_term = np.sin(sum(name_numbers) % 50)  # Add variation using sine

    print(f"Fractal Parameters: scale_x={scale_x}, scale_y={scale_y}, c_real={c_real}, c_imag={c_imag}")

    # Create the grid
    x = np.linspace(-scale_x, scale_x, size)
    y = np.linspace(-scale_y, scale_y, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Modified fractal equation with added variability
    C = complex(c_real / 10, c_imag / 10)
    fractal = np.zeros(Z.shape, dtype=int)

    for i in range(iterations):
        Z = Z**2 + C + extra_term  # Include variation
        Z += np.sin(Z) * noise_factor  # Add random noise
        Z = np.where(abs(Z) > 1000, 1000, Z)  # Clamp to avoid overflow
        fractal += abs(Z) < 1000  # Update fractal data

    return fractal

def dynamic_color_map(name_numbers):
    # Derive some seed values from the name
    base_color = sum(name_numbers) % 256

    # Confine the gradient to blues and adjusted purples
    gradient_colors = [
        f"#{int(base_color * 0.5):02x}00{base_color:02x}",  # Deep Purple (30% less red)
        f"#4B00{(base_color + 80) % 256:02x}",  # Indigo-like
        f"#6A0D{(base_color + 60) % 256:02x}",  # Amethyst Purple
        f"#8000{(base_color + 40) % 256:02x}",  # Deep Violet
        f"#0000{(base_color + 100) % 256:02x}",  # Dark Blue
        f"#4682B4",  # Steel Blue
        f"#87CEEB",  # Sky Blue
        f"#00008B",  # Deep Navy Blue
        f"#E6E6FA"   # Lavender (light purple)
    ]
    print(f"Generated Colors (Adjusted Purples and Blues): {gradient_colors}")
    return LinearSegmentedColormap.from_list("DynamicBluePurpleCmap", gradient_colors, N=256)

def auto_save_fractal(fractal, name):
    """Automatically save the fractal with a generated filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_fractal_{timestamp}.png"
    filepath = os.path.join("fractals", filename)
    os.makedirs("fractals", exist_ok=True)  # Ensure the directory exists
    plt.imsave(filepath, fractal, cmap="magma", format="png")
    print(f"Fractal saved as '{filepath}'!")

def plot_fractal(fractal, name, cmap):
    """Plot the fractal with a custom color map."""
    plt.figure(figsize=(8, 8))
    plt.imshow(fractal, cmap=cmap, extent=(-2, 2, -2, 2))
    plt.title(f"Fractal Art for {name}", fontsize=16)
    plt.axis("off")
    plt.show()

def main():
    """Main function to run the fractal generator."""
    while True:
        name = input("Enter your name (or 'exit' to quit): ").strip()
        if name.lower() == "exit":
            print("Exiting program.")
            break
        if not name:
            print("Please enter a valid name.")
            continue

        # Generate fractal based on name
        name_numbers = name_to_numbers(name)
        print(f"Numeric values for '{name}': {name_numbers}")
        fractal = generate_fractal(name_numbers)

        # Create a dynamic color map based on the name
        cmap = dynamic_color_map(name_numbers)

        # Plot and auto-save the fractal
        plot_fractal(fractal, name, cmap)
        auto_save_fractal(fractal, name)

if __name__ == "__main__":
    main()
