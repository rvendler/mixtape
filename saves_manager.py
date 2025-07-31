import os
import json

class SavesManager:
    SAVE_DIR = "saves"  # Default directory for saving states

    def __init__(self, name, force_empty = False):
        self.name = name
        self.state = {}
        self.ensure_save_dir()
        if force_empty:
            self.save()
        self.load()

    def ensure_save_dir(self):
        path = os.path.join(self.SAVE_DIR, self.name)
        if not os.path.exists(path):
            os.makedirs(path)

    def get_save_path(self, filename="data.json"):
        return os.path.join(self.SAVE_DIR, self.name, filename)

    @staticmethod
    def is_jsonable(x):
        try:
            json.dumps(x)
            return True
        except TypeError:
            return False

    def save(self):
        for key, value in self.state.items():
            if not self.is_jsonable(value):
                print(f"Can't write this to JSON: {key}")
        
        save_path = self.get_save_path()
        with open(save_path, 'w') as f:
            json.dump(self.state, f, default=lambda o: o.__dict__, indent=4)

    def load(self):
        save_path = self.get_save_path()
        if os.path.exists(save_path):
            with open(save_path, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {}

if __name__ == "__main__":
    manager = SavesManager("session1")
    manager.state["progress"] = 50
    manager.save()
    print(manager.state)