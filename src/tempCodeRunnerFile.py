from re import search
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import psycopg2
import sys
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import json
import os
import os.path