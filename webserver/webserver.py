# -*- coding: utf-8 -*-

from . import __version__
from pydantic import BaseModel
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from config import settings as conf
import sys
from selenium.webdriver import Firefox
from pilot.page_objects import FusionPBX


class Called(BaseModel):
    status: str
    callstatus: str
    message: str = None
    callid: str = None
    userfield: str = None
    id: str


security = HTTPBasic()


async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = False
    for user in conf.users:
        if secrets.compare_digest(credentials.username, user.name):
            correct_user = True
            break
    correct_password = secrets.compare_digest(credentials.password, user.password)

    if not (correct_user and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


try:
    conf.validators.validate()

except Exception as e:
    print(e)
    sys.exit(0)

browser = Firefox()
fusionpbx = FusionPBX(
    browser, conf.fusionpbx.url, conf.fusionpbx.user, conf.fusionpbx.password
)

app = FastAPI(
    title="Gnovit FusionPBX API",
    version=__version__,
    contact={
        "name": "Gnovit Open Source Consulting",
        "url": "https://gnovit.com",
        "email": "suporte@gnovit.com",
    },
)
origins = ["http://localhost", "http://localhost:8000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/api/users/me")
async def read_current_user(user: str = Depends(authenticate)):
    return f"{user}"


@app.get("/v1/domains/list")
async def domains_list(user: str = Depends(authenticate)):
    # f = FusionPBX(conf.fusionpbx.url, conf.fusionpbx.user, conf.fusionpbx.password)
    # domains = f.list_domains
    return fusionpbx.domains.list()


@app.put("/v1/domain/{domain}")
async def domain_create(domain: str, user: str = Depends(authenticate)):
    # create domain
    d = fusionpbx.domain.name = domain
    return d


@app.put("/v1/domain/{domain}/name/{new_name}")
async def domain_rename(domain: str, new_name: str, user: str = Depends(authenticate)):
    # rename domain
    d = fusionpbx.domain(domain)
    d.name = new_name
    return d


@app.delete("/v1/domain/{domain}")
async def domain_delete(domain: str, user: str = Depends(authenticate)):
    # delete domain
    d = fusionpbx.domain(domain)
    del d.name
    return d.name


@app.get("/v1/domain/{domain}/extensions/list")
async def extensions_list(domain: str, user: str = Depends(authenticate)):
    # list extensions
    d = fusionpbx.domain(domain)
    return d.extensions.list()
