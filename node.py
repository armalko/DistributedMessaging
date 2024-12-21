"""
This is a node file.
"""

import socket
import threading
import json
import web3_utils
from web3 import Web3

# Dictionary to store connected clients {receiver: socket}
clients = {}

# Lock to safely update the clients dictionary
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[Server] Connection established with {addr}")
    receiver = None  # To store the identifier for this client

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Parse the received data as JSON
            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                print("[Server] Received invalid JSON")
                continue

            if CALL_ETH and "bounty_claim" in message and "secret" in message:
                secret = message["secret"]
                eth_account = "0xYourPublicAddressHere"
                eth_private_key = "0xyourprivatekey... (Shhh!)"

                # Now redeem the bounty!
                web3_utils.redeem_bounty(
                    w3,
                    eth_account,
                    eth_private_key,
                    secret
                )

                print("Bounty redeemed!")
                continue

            # Validate the message structure
            if "text" not in message or "receiver" not in message or "secret" not in message:
                print("[Server] Invalid message format")
                continue

            # Handle the registration of the sender
            if receiver is None:
                receiver = message["receiver"]
                with clients_lock:
                    clients[receiver] = conn
                print(f"[Server] Registered client {receiver}")
                continue

            # Route the message to the intended receiver
            target = message["receiver"]
            with clients_lock:
                if target in clients:
                    try:
                        clients[target].sendall(data.encode())
                        print(f"[Server] Forwarded message to {target}")
                    except Exception as e:
                        print(f"[Server] Error sending to {target}: {e}")
                        with clients_lock:
                            del clients[target]
                else:
                    print(f"[Server] Receiver {target} not connected")
    except Exception as e:
        print(f"[Server] Error handling client {addr}: {e}")
    finally:
        # Clean up on client disconnect
        if receiver:
            with clients_lock:
                del clients[receiver]
        conn.close()
        print(f"[Server] Connection with {addr} closed")

def main():
    host = 'localhost'
    port = 12345  # Server port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[Server] Listening on {host}:{port}")


    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    CALL_ETH = False
    w3 = None

    if CALL_ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    main()
