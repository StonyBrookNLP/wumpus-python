import socket
import sys
import time

__author__ = 'chetannaik'

WAIT_TIME = 0.2

class Wumpus:
    def __init__(self):
        self.TCP_IP = '63.228.222.118'
        self.TCP_PORT = 9215
        self.BUFFER_SIZE = 10240
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logging = False

    def connect(self):
        try:
            self.conn.connect((self.TCP_IP, self.TCP_PORT))
            self.conn.send("\n")
            time.sleep(1)
            self.conn.recv(self.BUFFER_SIZE)
            print "Connected to Wumpus Server."
        except socket.error, msg:
            print """Couldn't connect with the socket-server: %s\n\
                terminating program""" % msg
            sys.exit(1)

    def disconnect(self):
        if self.conn:
            self.conn.close()
        print "Disconnected from Wumpus Server."

    def raw_query(self, wumpus_query):
        if not wumpus_query.endswith('\n'):
            wumpus_query += '\n'
        self.conn.send(wumpus_query)
        time.sleep(WAIT_TIME)
        data = self.conn.recv(self.BUFFER_SIZE)
        return data

    def set_buffer_size(self, buffer_size):
        self.BUFFER_SIZE = buffer_size

    def get(self, result_string, context):
        start_str, end_str = result_string.split()
        start = max(long(start_str) - context, 0)
        end = long(end_str) + context
        get_query = "@get {} {}".format(start, end)
        data = self.raw_query(get_query)
        splits = data.split("\n")
        if '' in splits: splits.remove('')
        if splits:
            return_list = [e for e in splits if e[0] and e[0] != '@'][0]
        else:
            return_list = []
        return return_list

    def query(self, wumpus_query, context=0):
        if not wumpus_query.endswith('\n'):
            wumpus_query += '\n'
        self.conn.send(wumpus_query)
        time.sleep(WAIT_TIME)
        data = self.conn.recv(self.BUFFER_SIZE)
        split_data = data.split("\n")
        if '' in split_data: split_data.remove('')
        filtered_list = [e for e in split_data if e[0] and e[0].isdigit()]
        return_sentences = []
        for e in filtered_list:
            return_list = self.get(e, context)
            return_sentences.append(return_list)
        return list(set(return_sentences))
