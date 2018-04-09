# otus.py.scoring_api

Scoring API for OTUS python education course.

Settings in ```constants.py```

To start server run ```python3 server.py```.

Default port ```8080```, all requests send to url   ```/method/```

Example requests:

```curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95", "arguments": {"phone": "79175002040", "email": "stupnikov@otus.ru", "first_name": "Стансилав", "last_name": "Ступников", "birthday": "01.01.1990", "gender": 1}}' http://127.0.0.1:8080/method/```

```curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "admin", "method": "clients_interests", "token": "fb7bd9a2432f1694ceb9573f02ea31ca47b1dd26ada49b266eb8b4537f68a87863aac604b43dac7b5e3cce97a57573c00a4d1cabbcbd15cb5d3c3974e8b85c6a", "arguments": {"client_ids": [1,2,3,4], "date": "20.07.2017"}}' http://127.0.0.1:8080/method/```

(To avoid ```Forbidden``` response just paste right token from console output, from string, begging from ```DIGEST```)