import tkinter as tk
from tkinter import ttk

def calculate_calories_and_macros():
    try:
        weight = float(weight_entry.get())
        phase = phase_var.get()

        if phase == "Cutting":
            protein_grams = weight * 1.2
            carb_grams = weight * 1.0
            fat_grams = weight * 0.2
            total_calories = (protein_grams * 4) + (carb_grams * 4) + (fat_grams * 9)
        elif phase == "Maintaining":
            protein_grams = weight * 1.0      # Updated value for maintaining
            carb_grams = weight * 1.6          # Updated value for maintaining
            fat_grams = weight * 0.35           # Updated value for maintaining
            total_calories = (protein_grams * 4) + (carb_grams * 4) + (fat_grams * 9)
        else:  # Bulking
            protein_grams = weight * 1.0  # Updated value for bulking
            carb_grams = weight * 2.0      # Updated value for bulking
            fat_grams = weight * 0.4        # Updated value for bulking
            total_calories = (protein_grams * 4) + (carb_grams * 4) + (fat_grams * 9)

        meal_ratios = [0.3, 0.3, 0.2, 0.2]
        meals = []

        for i, ratio in enumerate(meal_ratios, 1):
            meal_calories = int(total_calories * ratio)
            meal_protein = protein_grams * ratio
            meal_carbs = carb_grams * ratio
            meal_fat = fat_grams * ratio

            meals.append({
                'number': i,
                'calories': meal_calories,
                'protein': meal_protein,
                'carbs': meal_carbs,
                'fat': meal_fat
            })

        update_meal_labels(meals)
        total_label.config(text=f"Total Calories: {total_calories:.0f}")

        # Update daily goals
        daily_goals_label.config(text=(
            f"Daily Goals:\n"
            f"Protein: {protein_grams:.1f}g\n"
            f"Carbs: {carb_grams:.1f}g\n"
            f"Fat: {fat_grams:.1f}g"
        ))

    except ValueError:
        total_label.config(text="Please enter a valid weight")

def update_meal_labels(meals):
    for meal in meals:
        label = meal_labels[meal['number'] - 1]
        label.config(text=(
            f"Meal {meal['number']}: {meal['calories']} calories\n"
            f"Protein: {meal['protein']:.1f}g, "
            f"Carbs: {meal['carbs']:.1f}g, "
            f"Fat: {meal['fat']:.1f}g"
        ))

# Create the main window
root = tk.Tk()
root.title("Meal Calorie and Macronutrient Calculator")
root.geometry("400x400")

# Create and place widgets
weight_label = ttk.Label(root, text="Desired Weight (lbs):")
weight_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")

weight_entry = ttk.Entry(root, width=10)
weight_entry.grid(column=1, row=0, padx=5, pady=5)

phase_label = ttk.Label(root, text="Phase:")
phase_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")

phase_var = tk.StringVar()
# Increased width for better readability
phase_combobox = ttk.Combobox(root, textvariable=phase_var, values=["Cutting", "Maintaining", "Bulking"], state="readonly", width=15)
phase_combobox.grid(column=1, row=1, padx=5, pady=5)
phase_combobox.set("Maintaining")

calculate_button = ttk.Button(root, text="Calculate", command=calculate_calories_and_macros)
calculate_button.grid(column=0, row=2, columnspan=2, padx=5, pady=10)

meal_labels = []
for i in range(4):
    label = ttk.Label(root, text=f"Meal {i+1}: 0 calories\nProtein: 0g, Carbs: 0g, Fat: 0g")
    label.grid(column=0, row=i+3, columnspan=2, padx=5, pady=2, sticky="w")
    meal_labels.append(label)

total_label = ttk.Label(root, text="Total Calories: 0")
total_label.grid(column=0, row=7, columnspan=2, padx=5, pady=10)

# Daily goals label
daily_goals_label = ttk.Label(root, text="Daily Goals:\nProtein: 0g\nCarbs: 0g\nFat: 0g")
daily_goals_label.grid(column=0, row=8, columnspan=2, padx=5, pady=10, sticky="w")

# Start the GUI event loop
root.mainloop()
