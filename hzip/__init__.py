# This tool is usef for compression and decompression of text files using Huffman Algorithm

# Author : Chirag Vashist
# Repository : https://github.com/SerChirag/huffman-zip
# Liscence : GNU

import argparse, os.path, pickle 
from heapq import *
from collections import Counter, OrderedDict

##############
##data_types##
##############

forward = {}
reverse = {}

class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None
    
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class metadata:
    def __init__(self, codex, encoded_text, buffer):
        self.codex = codex
        self.encoded_text = encoded_text
        self.buffer = buffer


##############
###compress###
##############

def get_heap(text):
    ordered_list = Counter(text)
    h = []
    for i in ordered_list:
        node = HeapNode(i, ordered_list[i])
        heappush(h,node)
    return h

def generate_tree(h):
    while(len(h)>1):
        node1 = heappop(h)
        node2 = heappop(h)
        new_node = HeapNode(None, node1.freq + node2.freq)
        new_node.left = node1
        new_node.right = node2
        heappush(h,new_node)
    return heappop(h)
        
def generate_code(node,current):
    global forward,reverse
    if(node == None):
        return 

    if(node.char != None):
        forward[node.char] = current
        reverse[current] = node.char
        return

    generate_code(node.left, current + '0')
    generate_code(node.right, current + '1')


def encode(text,codex):
    encoded_text = ""
    for c in text:
        encoded_text += codex[c]
    buffer = 8 - len(encoded_text)%8
    encoded_text += '0'*buffer
    return bitstring_to_bytes(encoded_text),buffer

def bitstring_to_bytes(s):
    b = bytearray()
    for i in range(0, len(s), 8):
        byte = s[i:i+8]
        b.append(int(byte, 2))
    return bytes(b)


def compress(file_c,verbose):
    global forward,reverse
    filename = os.path.splitext(file_c)[0]
    output_path = str(filename) + ".hzip"
    with open(file_c, 'r+') as input_file, open(output_path, 'wb') as output_file, open("eileen", 'wb') as new_output_file:
        text = input_file.read()
        if(verbose):
            print "Creating Huffman Codes."
        h = get_heap(text)
        tree = generate_tree(h)
        generate_code(tree,'')
        if(verbose):
            print "Encoding File."
        encoded_text, buffer = encode(text,forward)
        metadata_obj = metadata(reverse,encoded_text,buffer)
        pickle.dump(reverse.items(),new_output_file)
        pickle.dump(metadata_obj,output_file,pickle.HIGHEST_PROTOCOL)
        if(verbose):
            print "Finished Encoding File."

##############
##decompress##
##############

def bytes_to_bitstring(encoded_text,buffer):
    decoded_data = ""
    for i in encoded_text:
        decoded_data += "{0:08b}".format(ord(i))
    return decoded_data[:len(decoded_data)-buffer]

def decode(reverse,encoded_text,buffer):
    decoded_data = bytes_to_bitstring(encoded_text,buffer)
    text = ""
    current = ""
    for bit in decoded_data:
        current += bit
        try:
            character = reverse[current]
            text += character
            current = ""
        except:
            pass
    return text


def decompress(file_d,verbose):
    filename = os.path.splitext(file_d)[0]
    output_path = filename + ".txt"
    with open(file_d, 'rb') as input_file, open(output_path, 'w') as output_file:
        if(verbose):
            print "Exctracting Metadata."
        data = pickle.load(input_file)
        if(verbose):
            print "Decoding Bytes to Text"
        text = decode(data.codex,data.encoded_text,data.buffer)
        if(verbose):
            print "Writing to File."
        output_file.write(text)        
    
##############
#####main#####
##############

def main():

    
    # Defining parser for command-line usage.:
    #     -c : For compression
    #     -d : For decompression
    #     --verbose : For verbosity
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store', dest='file_c',
                        help='Compresses a text file to a zip file')

    parser.add_argument('-d', action='store', dest='file_d',
                        help='De-compresses a zipped file to a text file')
    
    parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    results = parser.parse_args()

    #Compression Option Selected
    if(results.file_c):
        if(os.path.isfile(results.file_c)):
            extension = os.path.splitext(results.file_c)[1]
            if(extension != '.hzip'):
                compress(results.file_c,results.verbose)
            else:
                print "File is already compressed."
        else:
            print "File does not exist."

    #Decompression Option Selected
    if(results.file_d):
        if(os.path.isfile(results.file_d)):
            extension = os.path.splitext(results.file_d)[1]
            if(extension == '.hzip'):
                # print "Helo"
                decompress(results.file_d,results.verbose)
            else:
                print "Enter a valid .hzip file." 
        else:
            print "File does not exist."