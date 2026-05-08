"""Pytest configuration and path setup for tests."""
import sys
import os

tests_dir = os.path.dirname(__file__)
src_dir = os.path.join(tests_dir, "..")
sys.path.insert(0, src_dir)
