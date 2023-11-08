import tkinter as tk
import sqlite3
import tkinter.messagebox

# Create a class for each page
class Page(tk.Frame):
    def __init__(self, window, *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)
        self.window = window

    def show(self):
        self.lift()

class InventoryManager(Page):
    def __init__(self, window, *args, **kwargs):
        Page.__init__(self, window, *args, **kwargs)
        label = tk.Label(self, text="This is the Inventory Page")
        label.pack(side="top", fill="both", expand=True)
        self.ingredients = []
        self.inventory = []

        with open("database/ingredients.txt", "r") as file:
            self.ingredients = [line.strip() for line in file]

        label1 = tk.Label(self, text="Search for Ingredient:")
        label1.pack()

        self.entry1 = tk.Entry(self)
        self.entry1.pack()

        search_button = tk.Button(self, text="Search", command=self.search_ingredients)
        search_button.pack()

        self.results = tk.Listbox(self, height=10, width=40)
        self.results.pack()

        add_button = tk.Button(self, text="Add to Inventory", command=self.add_to_temp_list)
        add_button.pack()

        remove_button = tk.Button(self, text="Remove from Inventory", command=self.remove_from_temp_list)
        remove_button.pack()

        save_inventory_button = tk.Button(self, text="Save Inventory", command=self.save_inventory)
        save_inventory_button.pack()

        self.temp_list = tk.Listbox(self, height=10, width=40)
        self.temp_list.pack()

    def search_ingredients(self):
        query = self.entry1.get().strip()
        self.results.delete(0, tk.END)

        for ingredient in self.ingredients:
            if query.lower() in ingredient.lower():
                self.results.insert(tk.END, ingredient)

    def add_to_temp_list(self):
        selected_item = self.results.get(tk.ACTIVE)
        if selected_item:
            self.inventory.append(selected_item)
            self.temp_list.insert(tk.END, selected_item)
            self.results.delete(tk.ACTIVE)

    def remove_from_temp_list(self):
        selected_item = self.temp_list.get(tk.ACTIVE)
        if selected_item:
            self.inventory.remove(selected_item)
            self.temp_list.delete(tk.ACTIVE)
            self.results.insert(tk.END, selected_item)

    def save_inventory(self):
        with open("database/inventory.txt", "w") as file:
            for ingredient in self.inventory:
                file.write(ingredient + '\n')



class RecipeRetriever(Page):
    def __init__(self, window, *args, **kwargs):
        Page.__init__(self, window, *args, **kwargs)
        label = tk.Label(self, text="This is the Recipe Page")
        label.pack(side="top", fill="both", expand=True)

        check_for_recipe_button = tk.Button(self, text="Check for Recipe", command=self.check_for_recipe)
        check_for_recipe_button.pack()

        self.unique_results = tk.Listbox(self, height=10, width=40)
        self.unique_results.pack()
    
    def read_inventory(self):
        with open("database/inventory.txt", "r") as file:
            inventory = [str(line.strip()) for line in file]
        return inventory

    def check_for_recipe(self):
        inventory = self.read_inventory()

        if len(inventory) < 3:
            tkinter.messagebox.showinfo("Insufficient Ingredients", "Please add at least three ingredients to the inventory.")
            return
        
        conn = sqlite3.connect('database/recipes.db')
        c = conn.cursor()

        # Build the SQL query to search for recipes that contain the ingredient
        for i, ingredient in enumerate(inventory):
            query = "SELECT * FROM RAW_recipes WHERE ingredients LIKE '%" + ingredient + "%'"

        # Execute the query and get the results
        c.execute(query)
        results = c.fetchall()

        for name in results:
            with open("database/recipes_names.txt", "w") as file:
                file.write(name[0] + '\n')
                
                self.unique_results.insert(tk.END, name[0])

        # Close the database connection
        conn.close()

        # Return True if there are results, otherwise return False
        if len(results) > 0:
            return True
        else:
            return False

class MainView(tk.Frame):
    def __init__(self, window, *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)

        self.window = window

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        inventory_manager = InventoryManager(container)
        recipe_retriever = RecipeRetriever(container)

        inventory_manager.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        recipe_retriever.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Inventory", command=inventory_manager.lift)
        b2 = tk.Button(buttonframe, text="Recipes", command=recipe_retriever.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        inventory_manager.show()

if __name__ == "__main__":
    root1 = tk.Tk()
    root1.title("Inventory Manager")
    main1 = MainView(root1)
    main1.pack(side="top", fill="both", expand=True)
    root1.wm_geometry("400x400")

    root2 = tk.Tk()
    root2.title("Recipe Retriever")
    main2 = MainView(root2)
    main2.pack(side="top", fill="both", expand=True)
    root2.wm_geometry("400x400")

    root1.mainloop()
    #root2.mainloop()