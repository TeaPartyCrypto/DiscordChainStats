from threading import Thread

import circulatingsupply
import hashrate
import marketcap
import price
import volume

clients = {
    circulatingsupply.bot_token: circulatingsupply.client,
    hashrate.bot_token: hashrate.client,
    marketcap.bot_token: marketcap.client,
    volume.bot_token: volume.client,
    price.bot_token: price.client,
}

processes = []
for client in clients:
    if client != "" and client is not None:
        processes.append(Thread(target=clients[client].run, args=(client,)))

for process in processes:
    process.start()

for process in processes:
    process.join()
