#!/bin/bash
#compile file server script

g++ Main.cpp Client.cpp FileIO.cpp Log.cpp -lpthread -o "../bin/NFT"
echo "Done!"
