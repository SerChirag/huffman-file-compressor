# Huffman File Compressor

This package can be used to compress text files. The software uses Huffman Algorithm and provides loseless compression. 
Compression Ration is close to 50%.

## Installation

First, clone this repository to your machine.

    git clone https://github.com/SerChirag/huffman-zip
  
 Next, change the directory and install the package :  

    cd huffman-zip/
    sudo python setup.py install

## Usage

To compress a text, use the following command:

    hzip -c <filename.txt>

To decompress a zipped file, use the following command:

    hzip -d <filename.hzip>



