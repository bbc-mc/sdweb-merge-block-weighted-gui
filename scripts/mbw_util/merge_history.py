#
#
#
import os
import datetime
from csv import DictWriter, DictReader
import shutil

from modules import scripts


CSV_FILE_ROOT = "csv/"
CSV_FILE_PATH = "csv/history.tsv"
HEADERS = [
        "model_A", "model_A_hash", "model_A_sha256",
        "model_B", "model_B_hash", "model_B_sha256",
        "model_O", "model_O_hash", "model_O_sha256",
        "base_alpha", "weight_name", "weight_values", "weight_values2", "datetime"]
path_root = scripts.basedir()


class MergeHistory():
    def __init__(self):
        self.fileroot = os.path.join(path_root, CSV_FILE_ROOT)
        self.filepath = os.path.join(path_root, CSV_FILE_PATH)
        if not os.path.exists(self.fileroot):
            os.mkdir(self.fileroot)
        if os.path.exists(self.filepath):
            self.update_header()

    def add_history(self,
                model_A_name, model_A_hash, model_A_sha256,
                model_B_name, model_B_hash, model_B_sha256,
                model_O_name, model_O_hash, model_O_sha256,
                sl_base_alpha,
                weight_value_A,
                weight_value_B,
                weight_name=""):
        _history_dict = {}
        _history_dict.update({
            "model_A": model_A_name,
            "model_A_hash": model_A_hash,
            "model_A_sha256": model_A_sha256,
            "model_B": model_B_name,
            "model_B_hash": model_B_hash,
            "model_B_sha256": model_B_sha256,
            "model_O": model_O_name,
            "model_O_hash": model_O_hash,
            "model_O_sha256": model_O_sha256,
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
            # apply change
            if len(hist_data) > 0:
                # backup before change
                shutil.copy(self.filepath, self.filepath + ".bak")
                with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                    dw = DictWriter(f, fieldnames=HEADERS, delimiter='\t')
                    dw.writeheader()
                    dw.writerows(hist_data)
