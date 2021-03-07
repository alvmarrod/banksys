# -*- coding: utf-8 -*-
import os
import time
import pytest
import uvicorn
import logging
import requests
#import library.api
from multiprocessing import Process

#######################################################################

# Run server identically to main, so we can test the API
@pytest.fixture(scope="session")
def run_server():

    def start_server():
        uvicorn.run(
            "banksys.library.api:app", 
            host="0.0.0.0", 
            port=8080, 
            log_level="info"
        )

    def stop_server():
        proc.kill()

    request.addfinalizer(remove_config_test)

    proc = Process(target=start_server, args=(), daemon=True)
    proc.start()
    yield

#######################################################################

def test_health():

    time.sleep(5)

    response = requests.get("http://127.0.0.1:8080/health")
    assert response.status_code == 200
    assert len(response.json()["msg"]) > 0

#######################################################################