import Node

key_length=8

alice = Node.Node("Alice")
#bob = Node.Node("Bob")
david = Node.Node("David")

print("nodes created")

#KGP
alice.gen_key("Bob", key_length, "0")
print("first gen key done")
alice.gen_key("Bob", key_length, "1")
alice.gen_key("David", key_length, "0")
alice.gen_key("David", key_length, "1")
david.gen_key("Bob", key_length, "qkd")
print("all k done")

#key simm
david.send_key_part("bob", "alice", "0", length=0.5, crypt=david.keys["bob"]["qkd"])
bob.check_incoming(crypt=bob.keys["david"]["qkd"])
david.send_key_part("bob", "alice", "1", length=0.5, crypt=david.keys["bob"]["qkd"])
bob.check_incoming(crypt=bob.keys["david"]["qkd"])

bob.send_key_part("david", "alice", "0", length=0.5, crypt=bob.keys["david"]["qkd"])
david.check_incoming(crypt=david.keys["bob"]["qkd"])
bob.send_key_part("david", "alice", "1", length=0.5, crypt=bob.keys["david"]["qkd"])
david.check_incoming(crypt=david.keys["bob"]["qkd"])

alice.send_data("bob", "1", "david")
bob.check_incoming()
alice.send_data("david", "1", "bob")
david.check_incoming()

bob_result = bob.verify_messages()
print(bob_result)

david_result = david.verify_messages()
print(david_result)
