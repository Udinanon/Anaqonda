from cqc.pythonLib import CQCConnection, qubit
import random
import json
import time

class Node(object):

    def __init__(self, name):
        self.keys = dict()
        self.keys_others = dict()
        self.unverified_message = []
        self.name = name
    
    def gen_key(self, partner, key_length, tag):
        key = _gen_key(self, partner, int(key_length*7.5))
        while len(key) < key_length:
            temp = _gen_key(self, partner, int(7.5*(key_length - len(key))))
            key.append(temp)
        # trim, save, return
        self.keys[partner][tag] = key[0:key_length]
        return

    def _gen_key(self, partner, N_QUBIT):
        with open("n_qubit.config", "w+") as config_file:
            config_file.write(N_QUBIT)
        with CQCConnection(self.name) as Me:
            # Preparing my qubits
            h_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
            x_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
            q_vector = []
            
            for _ in range(N_QUBIT):
                q_vector.append(qubit(Me))
            
            for i in range(N_QUBIT):
                if x_vector[i] == 1:
                    q_vector[i].X()
                if h_vector[i] == 1:
                    q_vector[i].H()
            
            # Ask to Charlie (the commutor node as chosen for the network architecture)
            # if I am the master, stating who I am
            #print("~Alice  # Am I the master, stating who I am (?_?)")
            Me.sendClassical("Charlie", json.dumps( {"name": self.name} ).encode("utf-8"))
            charlie_attempt_response = Me.recvClassical()
            im_master = json.loads(charlie_attempt_response.decode("utf-8"))
            
            # If Charlie responded than it's ready for receiving my qubits, I send them
            #print("~Alice  # I'm sending the qubits to Charlie (T_T)")
            for qubit in q_vector:
                Me.sendQubit(qubit, "Charlie")
            
            # Receive the resulting matrix from Charlie
            matrix = json.loads(Me.recvClassical().decode("utf-8"))

            time.sleep(1)

            # Send vector H
            Me.sendClassical(partner, json.dumps(h_vector).encode("utf-8"))

            # Read vector H
            hother_vector = json.loads(Me.recvClassical().decode("utf-8"))

            if im_master:
                # Flips the necessary bits based on matrix correlation
                for i in range(N_QUBIT):
                    if matrix[i][1] == 0:
                        x_vector[i] = "b"
                        continue
                    if h_vector[i] != hother_vector[i]:
                        x_vector[i] = "h"
                        continue
                    if h_vector[i] == 1 and matrix[i][0] == 0:
                        continue
                    x_vector[i] = 1 if x_vector[i] == 0 else 0
            else:
                # Remove errors
                for i in range(N_QUBIT):
                    if matrix[i][1] == 0:
                        x_vector[i] = "b"
                        continue
                    if h_vector[i] != hother_vector[i]:
                        x_vector[i] = "h"
                        continue
            
            # Filtering key
            key = []
            for i in range(N_QUBIT):
                if type(x_vector[i]) is not str:
                    key.append(x_vector[i])

            # Print the key obtained
            #print("~Alice  # " + repr(key))
            #print("~Alice  # Key length: " + str(len(key)))
            
            if not im_master:
                simm_len = int(len(key)/3)
                Me.sendClassical(partner, json.dumps(key[0:simm_len]).encode("utf-8"))
                charlie_evil_str = json.loads(Me.recvClassical().decode("utf-8"))
                #print(charlie_evil_str)
                if charlie_evil_str == "CHARLIE EVIL":
                    print("~" + self.name + "  # " + self.name + " IS DESTROYING THE KEY, CHARLIE IS EVIL")
                    key = None
                else
                    key = key[simm_len:]

            else:
                simm_key = json.loads(Me.recvClassical().decode("utf-8"))
                simm_len = len(simm_key)
                #print("~Alice  # ARE SIMM_KEYS THE SAME? "+str(simm_key==key[0:simm_len]))
                err_counter = 0
                for i in range(simm_len):
                    if simm_key[i] != key[i]:
                        err_counter = err_counter + 1
                #print("~Alice  # QBER="+str(err_counter/simm_len))
                # Suppose perfect channel, no errors
                if err_counter == 0:
                    Me.sendClassical(partner, json.dumps("CHARLIE GOOD").encode("utf-8"))
                    key = key[simm_len:]
                else:
                    Me.sendClassical(partner, json.dumps("CHARLIE EVIL").encode("utf-8"))
                    print("~" + self.name + "  # " + self.name + " IS DESTROYING THE KEY, CHARLIE IS EVIL")
                    key = None
    
    def send_key_part(self, to, key_with, key_tag, length, crypt):
        key = self.keys[key_with][key_tag]
        end_index = int(len(key)*length)
        key_part_to_send = key[0:end_index]
        if len(crypt) < len(key_part_to_send):
            raise
        for i in len(key_part_to_send):
            key_part_to_send[i] ^= crypt[i]
        message = {
            "type": "key_part",
            "data": {"key": key_part_to_send, "key_with": key_with, "key_tag": key_tag},
            "from": self.name
            }
        with CQCConnection(self.name) as Me:
            Me.sendClassical(to, json.dumps(message).encode("utf-8"))

    def send_data(self, to, msg, auth):
        message = {
            "type": "signed_message",
            "data": {
                "msg": msg,
                "key_with_to": self.keys[to][msg],
                "key_with_auth": self.keys[auth][msg]
            },
            "from": self.name
        }
        with CQCConnection(self.name) as Me:
            Me.sendClassical(to, json.dumps(message).encode("utf-8"))

    def check_incoming(self, crypt=[]):
        message_recv = json.loads(Me.recvClassical().decode("utf-8"))
        if message_recv["type"] == "key_part":
            data = message_recv["data"]
            key_recv = data["key"]
            for i in len(key_recv):
                key_recv[i] ^= crypt[i]
            self.keys_others[data["key_with"]][data["key_tag"]] = key_recv
        else if message_recv["type"] == "signed_message":
            data = message_recv["data"]
            data["from"] = message_recv["from"]
            self.unverified_message.append(data)

    def verify_message(self, auth):
        results = []
        while len(self.unverified_message) > 0:
            data = self.unverified_message.pop()
            if data["key_with_to"] != self.keys[data["from"]][data["msg"]]:
                results.append({"msg": data["msg"], "status": False})
                continue
            key_part = self.keys_others[auth][data["msg"]]
            if data["key_with_auth"][0:len(key_part)] != key_part:
                results.append({"msg": data["msg"], "status": False})
                continue
            results.append({"msg": data["msg"], "status": True})
        return results
        