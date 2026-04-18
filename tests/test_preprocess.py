import os
import sys

def test_src_folder_exists():
    assert os.path.isdir("src"), "src folder should exist"

def test_app_file_exists():
    assert os.path.isfile("src/app.py"), "app.py should exist"

def test_preprocess_file_exists():
    assert os.path.isfile("src/preprocess.py"), "preprocess.py should exist"

def test_dvc_tracking_exists():
    assert os.path.isfile("models/saved.dvc"), "model should be DVC tracked"

def test_dockerfile_exists():
    assert os.path.isfile("Dockerfile"), "Dockerfile should exist"