import config
from analysis.dataAnalysis import analyze
import decoders.interleaved as decoder
from plotters.AmpPhaPlotter import Plotter
import os
import time


def process_pcap_file(pcap_filename, caminho, sequence):

    #pcap_filepath = '../scans'
   
    if '.pcap' not in pcap_filename:
        pcap_filename += '.pcap'
    pcap_filepath = '/'.join([caminho, pcap_filename])    
    try:
        samples = decoder.read_pcap(pcap_filepath)
    except FileNotFoundError:
        print(f'File {pcap_filepath} not found.')
        exit(-1)
    
    csi_data = samples.get_pd_csi()

    data1 = analyze(csi_data[0:250], sequence)

    data2 = analyze(csi_data[45:295], sequence)
    data3 = analyze(csi_data[90:340], sequence)

    data4 = analyze(csi_data[135:385], sequence)

    data5 = analyze(csi_data[180:410], sequence)
    data6 = analyze(csi_data[225:475], sequence)
    data7 = analyze(csi_data[250:500], sequence)

    return data1, data2, data3, data4, data5, data6, data7


    

    #function to check if next file exists. Wait until 15 seconds
def check_next_file(file_name):
    limit = 0
    while(limit <= 150):
        try:
            with open('./pcapfiles/' + file_name + '.pcap', 'r') as f:
                limit = 0
                return True
        except IOError:
            print("Waiting 0.25 seconds to receive next file")
            time.sleep(0.25)
            limit += 1
    print(limit)
    print("Timeout")
    return False


