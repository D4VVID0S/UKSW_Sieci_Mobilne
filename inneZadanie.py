import numpy as np
import matplotlib.pyplot as plt

class CitySimulator:
    def __init__(self, L, p):
        self.L = L  # Rozmiar siatki miasta
        self.p = p  # Prawdopodobieństwo blokady ulicy
        self.city_map = np.zeros((L, L))  # Inicjalizacja mapy miasta
        self.start = None  # Punkt początkowy
        self.end = None  # Punkt końcowy
        self.path = []  # Trasa przejazdu

    def generate_city(self):
        # Losowanie punktu początkowego i końcowego
        self.start = (np.random.randint(self.L), np.random.randint(self.L))
        self.end = (np.random.randint(self.L), np.random.randint(self.L))

    def find_shortest_path(self):
        # Implementacja algorytmu znajdującego najkrótszą ścieżkę (np. Dijkstra lub A*)
        # Zapisz znalezioną ścieżkę w self.path
        pass

    def simulate(self):
        self.generate_city()
        self.find_shortest_path()
        self.city_map[self.start] = 1  # Oznacz punkt początkowy na mapie
        self.city_map[self.end] = 2  # Oznacz punkt końcowy na mapie
        current_time = 0

        while self.path:
            current_location = self.path.pop(0)
            self.city_map[current_location] = 3  # Oznacz aktualną lokalizację pojazdu
            self.plot_city_map(current_time)
            self.city_map[current_location] = 0  # Usuń oznaczenie aktualnej lokalizacji

            if current_location == self.end:
                print("Pojazd dotarł do celu!")
                break

            next_location = self.path[0]
            if np.random.random() > self.p:
                self.path.insert(0, current_location)  # Jeśli ulica jest zablokowana, wróć do poprzedniej lokalizacji

            current_time += 1

    def plot_city_map(self, current_time):
        plt.imshow(self.city_map, cmap='tab10')
        plt.title(f"Symulator Miasta - Czas: {current_time}")
        plt.xlabel("Numer skrzyżowania")
        plt.ylabel("Czas")
        plt.xticks(np.arange(self.L))
        plt.yticks(np.arange(current_time + 1))
        plt.colorbar(ticks=[0, 1, 2, 3], label='Legenda', boundaries=[-0.5, 0.5, 1.5, 2.5, 3.5],
                     values=[0, 1, 2, 3])
        plt.grid(color='w', linewidth=1.5)
        plt.show()

# Użycie symulatora
simulator = CitySimulator(L=10, p=0.2)
simulator.simulate()
