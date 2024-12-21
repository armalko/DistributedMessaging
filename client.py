import socket
import threading
import json
import key_utils
import base64
import web3_utils
from web3 import Web3

def receive_messages(sock):
    """Thread to handle incoming messages from the server."""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            # Parse received JSON message
            try:
                message = json.loads(data)
                ciphertext = base64.b64decode(message['text'])
                print(f"[{message['receiver']}] {key_utils.decode_text(PRIVATE_KEY, ciphertext)}")

                if CALL_ETH:
                    encrypted_bounty = base64.b64decode(message['secret'])
                    secret_bounty = key_utils.decode_text(PRIVATE_KEY, encrypted_bounty)

                    message = {
                        "bounty_claim": "yes",
                        "secret": secret_bounty
                    }

                    try:
                        sock.sendall(json.dumps(message).encode())
                    except Exception as e:
                        print(f"[Client] Error sending message: {e}")
                        break


            except json.JSONDecodeError:
                print("[Client] Received invalid JSON")
        except Exception as e:
            print(f"[Client] Error receiving message: {e}")
            break

def send_messages(sock, receiver):
    """Send messages to the server."""
    print("[Client] You can start sending messages. Type 'exit' to quit.")
    while True:
        text = input("> ")
        if text.lower() == 'exit':
            break

        ciphertext = key_utils.encode_text(PUBLIC_KEY, text)
        ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')

        secret = ""

        if CALL_ETH:
            eth_account = "0xYourPublicAddressHere"
            eth_private_key = "0xyourprivatekey... (Shhh!)"
            secret_bounty = "Super Secret (Kirill the best!)"
            bounty_hash = w3.keccak(text=secret_bounty)

            from_hex_bounty = w3.toHex(bounty_hash)
            web3_utils.register_bounty(w3, eth_account, eth_private_key, from_hex_bounty)

            # Encoding bounty...
            ciphertext_secret = key_utils.encode_text(PUBLIC_KEY, text)
            secret = base64.b64encode(ciphertext_secret).decode('utf-8')

        message = {
            "text": ciphertext_base64,
            "receiver": receiver,
            "secret": secret
        }
        try:
            sock.sendall(json.dumps(message).encode())
        except Exception as e:
            print(f"[Client] Error sending message: {e}")
            break

def main(server_host, server_port, client_receiver, peer_receiver, secret):
    """Main client function."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print(f"[Client] Connected to server at {server_host}:{server_port}")

    # Register the client with the server
    registration_message = {
        "text": "register",
        "receiver": client_receiver,
        "secret": secret
    }
    client_socket.sendall(json.dumps(registration_message).encode())

    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Start sending messages to the peer
    send_messages(client_socket, peer_receiver)

    # Close the connection when done
    client_socket.close()
    print("[Client] Disconnected from server")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python3 client.py <server_host> <server_port> <client_receiver> <peer_receiver>")
        sys.exit(1)

    CALL_ETH = False
    w3 = None

    if CALL_ETH:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    client_receiver = sys.argv[3]  # Unique identifier for this client
    peer_receiver = sys.argv[4]  # The identifier of the peer to send messages to

    PRIVATE_KEY = key_utils.load_private_key_from_file(f"{client_receiver}_PRIVATE.pem")
    PUBLIC_KEY = key_utils.load_public_key_from_file(f"{peer_receiver}_PUBLIC.pem")

    main(server_host, server_port, client_receiver, peer_receiver, "Initial secret")
