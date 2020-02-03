from BlockchainController import BlockchainController

#metode
#ispis blok
def printBlock(block : dict()):
    print("Block Hash: " + block["hash"] + "\n" + "\t with " + str(len(block["tx"])) + " transactions")
#ispis mreza
def printNetworkInfo(networkInfo : dict()):
    print("Current network info:")
    print("\tNetwork active: " + str(networkInfo['networkactive']))
    print("\tNumber of connections: " + str(networkInfo['connections']))
    print("\tRelay fee: " + str(networkInfo['relayfee']))
    print("\tSubversion : " + str(networkInfo['subversion']))
#ispis blockchain
def printBlockchainInfo(blockchainInfo : dict()):
    print("Blockchain info:")
    print("\tName: " + str(blockchainInfo['chain']))
    print("\tNumber of blocks: " + str(blockchainInfo['blocks']))
    print("\tBest block hash: " + str(blockchainInfo['bestblockhash']))
#ispis transakcija
def printTransactionInfo(transaction : dict()):
    print("Transaction info:")
    print("\tID: " + str(transaction['txid']))
    # za svaki prijenos prema unutra
    for vin in transaction['vin']:
        # ispisi vrijednosti
        if 'value' in vin:
            print("\tIn value: " + str(vin['value']))
    # za svaki prijenos prema van
    for vout in transaction['vout']:
        # ispisi vrijendnosti
        if 'value' in vout:
            print("\tOut value: " + str(vout['value']))

# main START
host = "blockchain.oss.unist.hr"
port = 8332
username = "student"
password = "2B4DB3SmsM2B4DB3SmsM89QjgYFp89QjgYFp"

# bitchaincontrl START
blockchainController = BlockchainController(host, port)
# provjera konekcije
if blockchainController.tryConnectUser(username, password):
    # podaaci o mrezi
    printNetworkInfo(blockchainController.getNetworkInfo())
    # podaci o blockchainu
    printBlockchainInfo(blockchainController.getBlockchainInfo())
    # odabirem prve ili zadnje blokove
    option = input("F for first, L for last?\n").strip().upper()
    # odabirem broj blokova
    numOfBlocks = int(input("Number of blocks?\n"))
    blocks = []

    if option == "F":
        blocks = blockchainController.getFirstNBlocks(numOfBlocks)
    elif option == "L":
        blocks = blockchainController.getLastNBlocks(numOfBlocks)
    else:
        print("Unknown command!")

    # ispis blokova i njihovih transakcija
    for block in blocks:
        # ispisi blok
        printBlock(block)
        for transactionId in block["tx"]:
            transaction = blockchainController.getTransaction(transactionId)
            if transaction:
                printTransactionInfo(transaction)
else:
    # poruka ako se nisam uspo spojiti
    print("Could not connect!")
