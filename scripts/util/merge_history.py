#
#
#
import os
import datetime
from csv import DictWriter, DictReader

from modules import scripts


CSV_FILE_PATH = "csv/history.tsv"
HEADERS = ["model_A", "model_A_hash", "model_B", "model_B_hash", "model_O", "model_O_hash", "base_alpha", "weight_name", "weight_values", "weight_values2", "datetime"]
path_root = scripts.basedir()


class MergeHistory():
    def __init__(self):
        self.filepath = os.path.join(path_root, CSV_FILE_PATH)
        if os.path.exists(self.filepath):
            self.update_header()

    def add_history(self, model_A, model_B, model_O, model_O_hash, sl_base_alpha, weight_value_A, weight_value_B, weight_name=""):
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
            "weight_values": weight_value_A,
            "weight_values2": weight_value_B,
            "datetime": f"{datetime.datetime.now()}"
            })

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                dw.writeheader()
        # save to file
        with open(self.filepath, "a", newline="", encoding='utf-8') as f:
            dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
            dw.writerow(_history_dict)

    def update_header(self):
        hist_data = []
        if os.path.exists(self.filepath):
            # check header in case HEADERS updated
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                dr = DictReader(f, delimiter='\t')
                new_header = [ x for x in HEADERS if x not in dr.fieldnames ]
                if len(new_header) > 0:
                    # need update.
                    hist_data = [ x for x in dr]
            if len(hist_data) > 0:
                with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                    dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                    dw.writeheader()
                    dw.writerows(hist_data)
