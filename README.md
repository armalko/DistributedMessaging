# DistributedMessaging

Proof of concept project for HSE. Crypto based end-to-end encrypted messaging protocol

Here's a small documentation for this project. 

## TLDR

Concept for off-chain communicating with bounties on-chain. Best to show on example. 
Imagine two people (Alisa and Bob) want to communicate securely, without storing messages anywhere (and they love crypto!). They could of course use on-chain texting; However, it's reaally sloooow. So, they consider following scheme:

- Write ERC-based token and deploy it.
- Contract has functionality of bounties. E.g. one can set secret Bounty Code that can be redeemed to get 1 token.
- Alisa sets bounty in this contract and encrypts it and message using RSA.
- Node (which has financial interest in retranslating messages) resends encrypted message to Bob.
- Bob decrypts message and bounty code and sends in back to Node.
- Node redeems code.
- Everyone happy!

Now to the point (realisation of this concept in Python).

## Project structure

Project constists of following files:

- node.py : Node script, that suits as retranslator of messages between clients. Able to redeem bounty codes, given by clients in return for sending messages.
- client.py : Client code. Connects to node via given port (e.g., 12345) and able to create bounty code, send messages and encrypt (decrypt) them.
- main.py : Useful for generating pairs of keys for users. Check inside for exact usage.
- contract.sol : Contract code (solidity).
- key_utils.py : Useful functions for encrypting/decrypting messages and generating keys using RSA.
- web3_utils : File with web3 connection functions.

## Usage

First, check if you have installed neccessary libraries.

```
pip3 install -r requirements.txt
```

Now let's generate key pairs.

```
python3 main.py Y user_1 user_2
```

We are ready to start the server node.

```
python3 node.py
```

Open another terminal window (CTRL + N) and start client1 and client2.

```
python client.py localhost 12345 user_1 user_2
```

And another one...

```
python client.py localhost 12345 user_2 user_1
```

You are ready to test!

## To Be Done

- Batches in code redeeming
- More then 2 clients
- Broadcasting (e.g. open channels)
- 

