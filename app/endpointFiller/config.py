import os
DOMAIN = "http://127.0.0.1"
PORT = "32800"
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_data_path = os.path.join(current_dir, "..", "..", "data")
BASE_DIR = relative_data_path