# UDP Ping application
## Client.py
Connects to a either a specified address of the form "addr:port", or a default address of "127.0.0.1:1200", then sends 10 udp messages, and calculates response time for each
## Server.py
A UDP server which echoes back any received message to the destination. Simulates a 30% datagram loss rate