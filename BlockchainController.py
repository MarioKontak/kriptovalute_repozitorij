from bitcoinrpc.authproxy import AuthServiceProxy 

class BlockchainController: 

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # connect
    def tryConnectUser(self, userName, password):
        try:
            # formatiranje url-a uz username i pass
            fullUrl = "http://{}:{}@{}:{}".format(userName, password, self.host, self.port)
            # kreiramo klijent
            self.blockchainClient=AuthServiceProxy(fullUrl)
            self.blockchainClient.getblockhash(0)
        except Exception as e:#ukoliko imamo exception
            return False
        return True

    # dohvat prvih N blokova transakcija, za n = 0 dohvat svih transakcija
    def getFirstNBlocks(self, n = 0):
        firstBlockHash = self.blockchainClient.getblockhash(0)
        chain=[]

        if firstBlockHash:
            firstBlock = self.blockchainClient.getblock(firstBlockHash)
            chain.append(firstBlock)
            currentBlock = firstBlock

            numBlocksToGet = self.blockchainClient.getblockcount() if n == 0 else n
            
            i = 1
            while currentBlock['nextblockhash'] and i < numBlocksToGet:
                nextBlockHash = currentBlock['nextblockhash']
                currentBlock = self.blockchainClient.getblock(nextBlockHash)
                chain.append(currentBlock)
                i += 1
        return chain

    # dohvat zadnjih N zadnjih blokova transakcija
    def getLastNBlocks(self, n: int):
        chain = []
        blockCount = self.blockchainClient.getblockcount()
        #hash zadnjeg bloka radi dohvata tog zadnjeg bloka
        lastBlockHash = self.blockchainClient.getblockhash(blockCount - 1)
        
        if lastBlockHash:
            lastBlock = self.blockchainClient.getblock(lastBlockHash)
            chain.append(lastBlock)
            currentBlock = lastBlock
            
            i = 1
            while currentBlock['previousblockhash'] and i < n:
                previousBlockHash = currentBlock['previousblockhash']
                currentBlock = self.blockchainClient.getblock(previousBlockHash)
                chain.append(currentBlock)
                i += 1
        return chain