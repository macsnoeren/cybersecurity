# ESP32S2 WEMOS S2 MINI (LOLIN S2)

This project is based on the ESP-IDF framework from Espressif created with Visual Studio Code.

The public and private keys are also pushed to the repo for demo purposes, so you can try it out.

## Workings

The main.c application is the firmware for the ESP32S2 and it will use the 2048 public key to encrypt a
message. This public key is hardcoded. 

At the server side, there is a python script server.py. Inside this script the private 2048 key is used. You can copy
the output of the ESP32S2 and try to decrypt it. Some examples are in as well. The python script uses the lib rsa and
it is able to decrypt the message. 

This way it is possible to get a secret across the other side. Note that RSA is not post Quantum proof.

## Generating your own keys
```bash
openssl genrsa -out key-2048.pem 2048
openssl rsa -in key.pem -outform PEM -pubout -out public-2048.pem
```

## Output ESP32S2
```
Base64!!
Result: 'iyldkxTKwNm7mhtdY/7epg8qK0vGGNrD5jg+U3V8umbEQJxmtoUYtFPdKTlxoeNQEGxMDCpaKclW9v9RGz6HrXAnTS/11vGdhTEYI2ljrmv3TXGn85mo4DKKNX6kHH91zn8dLFDTe7mw0gUfJMCFPghBT3YnEyCzN2EqszLAVRRwgUFYbeys8K0kP2Ox32CZi3u4HsIJ7oIgC1gaJZTXGupUX4zGcC1AJ00l0kev+CEoceZSGRC82KuJ3waCGY3vrvCet/+4Pgc6yG4HhbT0EF1j5q4I+es4JN6tU+At3Y36iqttGkGPXT6vw3If7G/q0n1LuA7xJVxkCJZiXNit+Q=='
```

## Output python
```
PS C:\Data\projects\ESPIDFESPS2TEST> & C:/Python310/python.exe c:/Data/projects/ESPIDFESPS2TEST/main/server.py
b'hQL7ro8mq7nf/SutkA/Grg/1CCQtLFqGwVxEushU10wBGElq5ktYeE67N+i6RG3ReSk1O3TRlaMYhzKsqvl09pVMZNNH556lHR2MHethzDZK7PyhtYzjuRYSQSBWqjUKbNGzc8GJrN3m0zifKj60eKYTJI+rqHJqtf24diEhsxo4T7U6gdUPhjUyNxtWkUunqXE+ZwyGiu3haILyouG8Qv1Jkur9+GWSY9ocDP6trSz8uhTv/sSOqEw+4+qCti5bHBIDuuTBPpWgDYlZKK74MFgFxWqe3oKG7KTUg/XMIIcMZkIbNl3mYBmC9KTK1SiftEWdCVHh+lkPkuaAf9AD4w=='
b'hello Bob!'
b'Dit is de ESP32S2 talking!\n'
b'Dit is de ESP32S2 talking!\n'
b'Dit is de ESP32S2 talking!!\n'
```

Good luck with the example!
