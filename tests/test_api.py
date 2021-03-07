# -*- coding: utf-8 -*-
import os
import time
import pytest
import uvicorn
import logging
import requests
#import library.api
from multiprocessing import Process

# https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest
#######################################################################
# Run server identically to main, so we can test the API
#######################################################################

def run_server():
    uvicorn.run(
        "banksys.library.api:app", 
        host="0.0.0.0", 
        port=8080, 
        log_level="info"
    )

@pytest.fixture()
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start() 
    yield
    proc.kill() # Cleanup after test

#######################################################################

def test_health(server):

    response = requests.get("http://127.0.0.1:8080/health")
    assert response.status_code == 200
    assert len(response.json()["msg"]) > 0

#######################################################################