from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    },
    solc_version="0.6.0",
)

#print (compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/6bd2630c9c9c41a591948d6084911d2a'))
chain_id = 11155111
my_address = '0xAc2D28b176D0eb0fc3D3295ADd614786d17c200C'
private_key = os.getenv('PRIVATE_KEY')
# print(private_key)
# private_key = '0xcb4f829d1e7914f76c7acb5f4b46249187367ccc0588a95a829ca13646c02aac'

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

nonce = w3.eth.get_transaction_count(my_address)
# print(nonce, '\n')
print('Deploying contract....')
transaction = SimpleStorage.constructor().build_transaction({'chainId':chain_id, 'from':my_address, 'nonce': nonce}
                                                            )
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Deployed!')
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())
# print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).build_transaction(
    {'chainId': chain_id, 'from': my_address, 'nonce': nonce+1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())