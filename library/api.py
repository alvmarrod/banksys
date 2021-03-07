import os
import logging
import datetime as dt

from fastapi import FastAPI

if "banksys" in __name__:
    import banksys.library.analysis as analysis
else:
    import library.analysis as analysis

#######################################################################

app = FastAPI(debug=False)

#######################################################################

@app.get("/health")
def health():
    now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return {
        "msg": f"Health response issued at server time: {now}"
    }

########################## GET SERVICES ##########################



########################## POST SERVICES ##########################