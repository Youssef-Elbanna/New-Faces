# phases/phase1.py
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.services.warc_service import WARCService

def run_phase1():
    print("=== Phase 1: Downloading and extracting HTML + images ===")
    service = WARCService()
    mappings = service.process_warc_files()
    print(f"Phase 1 complete. {len(mappings)} pages processed.")
