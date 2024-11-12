import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import seaborn as sns


"""    
Graphics - Final Version
"""

'''
This Function Visualizes the dictionary in a formatted style with keys and values aligned in columns
'''
def visualize_dictionary(data):
    num_columns = 2
    num_rows = len(data) // num_columns + (len(data) % num_columns > 0)
    keys = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    text_properties = dict(horizontalalignment='center', verticalalignment='center', fontsize=12,
                           fontfamily='monospace')
    fig.patch.set_facecolor('white')
    ax.set_title('Shormters', fontsize=20, color='black', pad=20)

    for i in range(len(data)):
        row = i % num_rows
        col = i // num_rows
        x = col * 0.5
        y = 1 - (row / num_rows) - 0.05
        color = 'red'

        ax.text(x, y, f"$X_{{{i + 1}}}$ =  {values[i]}", color=color, **text_properties)

    plt.grid(visible=False)
    plt.box(True)
    plt.tight_layout()
    plt.show()


'''
This Function Visualizes a subset of the given dictionary of shortmers in a decorated matrix.
'''
def visualize_alphabet(alphabet, num_sigmas=20):
    # Select a random sample of sigmas
    random_sigmas = random.sample(list(alphabet.keys()), num_sigmas)

    # Filter the alphabet to only include the selected sigmas
    filtered_alphabet = {sigma: alphabet[sigma] for sigma in random_sigmas}

    # Create a set of all shortmers
    all_shortmers = [f"X{i}" for i in range(1, 17)[::-1]]

    # Create a DataFrame with shortmers as rows and sigmas as columns
    df = pd.DataFrame(0, index=all_shortmers, columns=filtered_alphabet.keys())

    # Fill the DataFrame with presence (1) of shortmers
    for sigma, shortmers in filtered_alphabet.items():
        for shortmer in shortmers:
            df.at[shortmer, sigma] = 1

        # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df, cmap="Greens", cbar=False, linewidths=0.5, linecolor='black', square=True)

    plt.xlabel('Alphabet', fontsize=14, fontweight='bold')
    plt.ylabel('Shortmers', fontsize=14, fontweight='bold')
    plt.title(f'Shortmer Presence Across {num_sigmas} Random Sigmas', fontsize=16, fontweight='bold')

    # Customize tick labels
    ax = plt.gca()
    ax.set_xticklabels(
        [f'σ$_{{{i.get_text()[1:]}}}$' for i in ax.get_xticklabels()],
        rotation=45,
        fontsize=12,
        fontweight='bold'
    )
    ax.set_yticklabels(
         [f'X$_{{{i.get_text()[1:]}}}$' for i in ax.get_yticklabels()],
         rotation=0,
         fontsize=12,
         fontweight='bold'
    )

    plt.show()

'''
This function represents statics and comparison between two shortmers
'''
def compare_shortmers(dict1, dict2):
    letters = list(dict1.keys())
    random_letter = random.choice(letters)

    shortmers1 = dict1[random_letter]
    shortmers2 = dict2[random_letter]

    shortmer_names = list(set(shortmers1.keys()) | set(shortmers2.keys()))
    counts1 = [shortmers1.get(name, 0) for name in shortmer_names]
    counts2 = [shortmers2.get(name, 0) for name in shortmer_names]

    x = np.arange(len(shortmer_names))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, counts1, width, label='Dict1', color='blue', alpha=0.7)
    ax.bar(x + width / 2, counts2, width, label='Dict2', color='orange', alpha=0.7)

    ax.set_xlabel('Shortmers')
    ax.set_ylabel('Counts')
    ax.set_title(f'Shortmer counts for letter {random_letter}')
    ax.set_xticks(x)
    ax.set_xticklabels(shortmer_names)
    ax.legend()

    plt.tight_layout()
    plt.show()
