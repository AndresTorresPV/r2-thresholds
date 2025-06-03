#!/bin/bash
curl -X POST http://127.0.0.1:8000/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MESSAGE",
    "message": {
      "text": "'"$1"'"
    },
    "space": {
      "name": "spaces/local-test"
    },
    "user": {
      "displayName": "Jaime Torres"
    }
  }'
