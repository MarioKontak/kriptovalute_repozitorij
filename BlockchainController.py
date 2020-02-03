from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# upravljaci razred za rpc
class BlockchainController: 

    def __init__(self, host, port): # konstruktor
        self.host = host
        self.port = port

    # metoda za povezivanje na host, true uspjeno
    def tryConnectUser(self, userName, password):
        try:
            # formatiranje url-a uz username i pass
            fullUrl = "http://{}:{}@{}:{}".format(userName, password, self.host, self.port)
            # ovdje generiram klijenta
            self.blockchainClient=AuthServiceProxy(fullUrl)
            # poziv jednostavne operacije kako bi se potvrdilo povezivanje
            # ako se ovdje baci Exception nismo se povezali
            self.blockchainClient.getblockhash(0)
        except Exception as e:#nema povezivanja ako je exepction
            return False
        return True

    # dohvat podataka o mrezi
    def getNetworkInfo(self):
        return self.blockchainClient.getnetworkinfo()
    # dohvat podataka o chainu
    def getBlockchainInfo(self):
        return self.blockchainClient.getblockchaininfo()
    # dohvat transakcije po txid-u
    def getTransaction(self, id : str):
        try:
            # dohvacam raw transakciju
            rawTransaction = self.blockchainClient.getrawtransaction(id)
            # dkonverzija
            return self.blockchainClient.decoderawtransaction(rawTransaction)
        except JSONRPCException:
            return None

    # dohvat prvih N blokova
    def getFirstNBlocks(self, n = 0):#n=0 sve trensakcije
        # hash prvog bloka
        firstBlockHash = self.blockchainClient.getblockhash(0)
        chain=[]

        # pod uvjetom da postoji prvi blok
        if firstBlockHash:
            firstBlock = self.blockchainClient.getblock(firstBlockHash)
            chain.append(firstBlock)
            currentBlock = firstBlock

            # ovisno o opciji 'n' koliko blokova moramo dohvatiti
            numBlocksToGet = self.blockchainClient.getblockcount() if n == 0 else n
            i = 1
            # dok god imamo sljedeci blok i dok god nismo dohvatili dovoljan broj blokova
            while currentBlock['nextblockhash'] and i < numBlocksToGet:
                # hash sljedeceg bloka
                nextBlockHash = currentBlock['nextblockhash']
                # dohvati sljedeci blok pomocu hasha
                currentBlock = self.blockchainClient.getblock(nextBlockHash)
                chain.append(currentBlock)
                i += 1

        return chain

    # dohvaca N zadnjih blokova transakcija
    def getLastNBlocks(self, n: int):
        chain = []
        blockCount = self.blockchainClient.getblockcount()
        lastBlockHash = self.blockchainClient.getblockhash(blockCount - 1)
        
        # pod uvjetom da postoji zadnji blok
        if lastBlockHash:
            lastBlock = self.blockchainClient.getblock(lastBlockHash)
            chain.append(lastBlock)
            currentBlock = lastBlock
            
            i = 1
            # dok imam prosli blok i dok god nisam dobio dovoljno blokova 
            while currentBlock['previousblockhash'] and i < n:
                # hash prethodnog bloka
                previousBlockHash = currentBlock['previousblockhash']
                # dohvacam trenutni blok preko hasha
                currentBlock = self.blockchainClient.getblock(previousBlockHash)
                chain.append(currentBlock)
                i += 1

        return chain