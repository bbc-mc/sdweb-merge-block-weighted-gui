#
#
#
import os
from csv import DictReader

from modules import scripts


CSV_FILE_PATH = "csv/preset.tsv"
MYPRESET_PATH = "csv/preset_own.tsv"
HEADER = ["preset_name", "preset_weights"]
path_root = scripts.basedir()


class PresetWeights():
    def __init__(self):
        self.presets = {}

        if os.path.exists(os.path.join(path_root, MYPRESET_PATH)):
            with open(os.path.join(path_root, MYPRESET_PATH), "r") as f:
                reader = DictReader(f, delimiter="\t")
                lines_dict = [row for row in reader]
                for line_dict in lines_dict:
                    _w = ",".join([f"{x.strip()}" for x in line_dict["preset_weights"].split(",")])
                    self.presets.update({line_dict["preset_name"]: _w})

        with open(os.path.join(path_root, CSV_FILE_PATH), "r") as f:
            reader = DictReader(f, delimiter="\t")
            lines_dict = [row for row in reader]
            for line_dict in lines_dict:
                _w = ",".join([f"{x.strip()}" for x in line_dict["preset_weights"].split(",")])
                self.presets.update({line_dict["preset_name"]: _w})

    def get_preset_name_list(self):
        return [k for k in self.presets.keys()]

    def find_weight_by_name(self, preset_name=""):
        if preset_name and preset_name != "" and preset_name in self.presets.keys():
            return self.presets.get(preset_name, ",".join(["0.5" for _ in range(25)]))
        else:
            return ""

    def find_names_by_weight(self, weights=""):
        if weights and weights != "":
            if weights in self.presets.values():
                return [k for k, v in self.presets.items() if v == weights]
            else:
                _val = ",".join([f"{x.strip()}" for x in weights.split(",")])
                if _val in self.presets.values():
                    return [k for k, v in self.presets.items() if v == _val]
                else:
                    return []
        else:
            return []
