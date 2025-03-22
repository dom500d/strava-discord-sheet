import json
import os

class FileCache:
    def __init__(self, cache_file="cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=4)

    def get(self, key, default):
        return self.cache.get(key, default)

    def set(self, key, value):
        self.cache[key] = value
        self._save_cache()

    def delete(self, key):
         if key in self.cache:
            del self.cache[key]
            self._save_cache()

    def clear(self):
        self.cache = {}
        self._save_cache()