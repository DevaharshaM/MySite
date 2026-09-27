import os

edge_dir = "EdgeCases"
if os.path.exists(edge_dir):
    for item in sorted(os.listdir(edge_dir)):
        item_path = os.path.join(edge_dir, item)
        if os.path.isdir(item_path):
            files = os.listdir(item_path)
            print(f"{item}/: {files}")
