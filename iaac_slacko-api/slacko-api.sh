#!/bin/bash
cd /opt/slacko-api/
uvicorn main:app --host 0.0.0.0 --reload
