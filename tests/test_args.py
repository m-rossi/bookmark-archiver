import subprocess
import json

from .fixtures import *

def test_depth_flag_is_accepted(process):
    arg_process = subprocess.run(["archivebox", "add", "https://example.com", "--depth=0"], capture_output=True)
    assert 'unrecognized arguments: --depth' not in arg_process.stderr.decode("utf-8")

def test_depth_flag_fails_if_it_is_not_0_or_1(process):
    arg_process = subprocess.run(["archivebox", "add", "https://example.com", "--depth=5"], capture_output=True)
    assert 'invalid choice' in arg_process.stderr.decode("utf-8")
    arg_process = subprocess.run(["archivebox", "add", "https://example.com", "--depth=-1"], capture_output=True)
    assert 'invalid choice' in arg_process.stderr.decode("utf-8")

def test_depth_flag_0_crawls_only_the_arg_page(tmp_path, process):
    arg_process = subprocess.run(["archivebox", "add", "https://example.com", "--depth=0"], capture_output=True)
    archived_item_path = list(tmp_path.glob('archive/**/*'))[0]
    with open(archived_item_path / "index.json", "r") as f:
        output_json = json.load(f)
    assert output_json["base_url"] == "example.com"

def test_depth_flag_1_crawls_the_page_AND_links(tmp_path, process):
    arg_process = subprocess.run(["archivebox", "add", "https://example.com", "--depth=1"], capture_output=True)
    with open(tmp_path / "index.json", "r") as f:
        archive_file = f.read()
    assert "https://example.com" in archive_file
    assert "https://www.iana.org/domains/example" in archive_file