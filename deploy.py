from solcx import compile_standard, install_solc
import json
from web3 import Web3

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

w3 = Web3(Web3.HTTPProvider('127.0.0.1:7545'))
chain_id = 5777
my_address = '0x2e8990Fc92e0044866021e268811A90d52DF89a7'
private_key = '0xcb4f829d1e7914f76c7acb5f4b46249187367ccc0588a95a829ca13646c02aac'

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

nonce = w3.eth.get_transaction_count(my_address)
print(nonce)