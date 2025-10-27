import copy

# Representasi state adalah alokasi setiap barang ke salah satu kontainer
class State:
    def __init__(self, kontainer_list):
        self.kontainer_list = kontainer_list

    def clone(self):
        return State(copy.deepcopy(self.kontainer_list))

    def total_kontainer(self):
        return len(self.kontainer_list)

    def __repr__(self):
        result = ""
        for i, k in enumerate(self.kontainer_list, start=1):
            result += f"Kontainer {i}: {k}\n"
        return result
