#
#
#
import os
from csv import DictWriter, writer

from modules import scripts


CSV_FILE_PATH = "csv/history.tsv"
HEADERS = ["model_A", "model_A_hash", "model_B", "model_B_hash", "model_O", "model_O_hash", "base_alpha", "weight_name", "weight_values"]
path_root = scripts.basedir()


class MergeHistory():
    def __init__(self):
        self.filepath = os.path.join(path_root, CSV_FILE_PATH)

    def add_history(self, model_A, model_B, model_O, model_O_hash, sl_base_alpha, weight_values, weight_name=""):
        _history_dict = {}
        _history_dict.update({
            "model_A": f"{os.path.basename(model_A.split(' ')[0])}",
            "model_A_hash": f"{model_A.split(' ')[1]}",
            "model_B": f"{os.path.basename(model_B.split(' ')[0])}",
            "model_B_hash": f"{model_B.split(' ')[1]}",
            "model_O": model_O,
            "model_O_hash": model_O_hash,
            "base_alpha": sl_base_alpha,
            "weight_name": weight_name,
            "weight_values": weight_values,
            })

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                wr = writer(f, fieldnames=HEADERS, delimiter='\t')
                wr.writerow(HEADERS)
        # save to file
        with open(self.filepath, "a", newline="", encoding='utf-8') as f:
            dictwriter = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
            dictwriter.writerow(_history_dict)
