from web3 import Web3
from dotenv import load_dotenv
import os, json

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# 去掉前後空白/換行，避免 ENS 解析錯誤
if CONTRACT_ADDRESS:
    CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS.strip())
else:
    raise ValueError("❌ CONTRACT_ADDRESS 沒有設定，請檢查 .env")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# 測試連線
if not w3.is_connected():
    raise ConnectionError("❌ Web3 沒有連上節點，請檢查 INFURA_URL")
else:
    print("✅ 已連線到區塊鏈節點")

account = w3.eth.account.from_key(PRIVATE_KEY)
address = account.address

with open("NoteChainABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def add_note_on_chain(content: str):
    tx = contract.functions.addNote(content).build_transaction({
        "from": address,
        "nonce": w3.eth.get_transaction_count(address),
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)

def get_all_notes():
    notes = contract.functions.getAllNotes().call()
    result = []
    for n in notes:
        result.append({
            "id": n[0],
            "content": n[1],
            "timestamp": n[2]
        })
    return result
