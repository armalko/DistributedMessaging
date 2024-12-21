import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Replace with your actual contract ABI and deployed address
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "initialSupply",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "redeemer",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "solution",
				"type": "string"
			}
		],
		"name": "BountyRedeemed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "registrant",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "bountyHash",
				"type": "bytes32"
			}
		],
		"name": "BountyRegistered",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "bountyActive",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "currentBountyHash",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "solution",
				"type": "string"
			}
		],
		"name": "redeemBounty",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_bountyHash",
				"type": "bytes32"
			}
		],
		"name": "registerBounty",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
contract_address = "0x123456789abcdef123456789abcdef123456789a"


def register_bounty(
    w3: Web3,
    sender_address: str,
    private_key: str,
    bounty_hash: str
):
    """
    Calls the 'registerBounty(bytes32 _bountyHash)' function on the contract.

    :param w3: Web3 instance
    :param sender_address: The public address of the user registering the bounty
    :param private_key: The private key of the user (for transaction signing)
    :param bounty_hash: The keccak256 hash (in hex or bytes32 form) of the desired solution
    :return: Transaction receipt
    """
    # Prepare the contract object
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Get the nonce for the sender (to prevent transaction replay)
    nonce = w3.eth.get_transaction_count(sender_address)

    # Build the transaction data
    # Adjust gas and gasPrice as appropriate for your network
    txn = contract.functions.registerBounty(bounty_hash).buildTransaction({
        "from": sender_address,
        "nonce": nonce,
        "gas": 300000,  # Overestimate to be safe
        "gasPrice": w3.toWei("10", "gwei")
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)

    # Send the raw transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent: {tx_hash.hex()}")

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction mined. Block number: {tx_receipt.blockNumber}")

    return tx_receipt


# -------------------------------------------------------------------
# 2. Function to call RedeemBounty
# -------------------------------------------------------------------
def redeem_bounty(
    w3: Web3,
    sender_address: str,
    private_key: str,
    solution_str: str
):
    """
    Calls the 'redeemBounty(string calldata solution)' function on the contract.

    :param w3: Web3 instance
    :param sender_address: The public address of the user redeeming the bounty
    :param private_key: The private key of the user (for transaction signing)
    :param solution_str: The plaintext string whose keccak256 should match the bounty hash
    :return: Transaction receipt
    """
    # Prepare the contract object
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Get the nonce for the sender
    nonce = w3.eth.get_transaction_count(sender_address)

    # Build the transaction data
    txn = contract.functions.redeemBounty(solution_str).buildTransaction({
        "from": sender_address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.toWei("10", "gwei")
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)

    # Send the raw transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent: {tx_hash.hex()}")

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction mined. Block number: {tx_receipt.blockNumber}")

    return tx_receipt

