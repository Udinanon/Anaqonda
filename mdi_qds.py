key_length=20

alice=Node("Alice")
bob=Node("Bob")
charlie=Charlie()
david=Node("David")
#KGP
alice.gen_key("bob", key_length, "0")
alice.gen_key("bob", key_length, "1")
alice.gen_key("david", key_length, "0")
alice.gen_key("david", key_length, "1")
david.gen_key("bob", key_length, "qkd")
#key simm
david.send_key_part("bob", david.keys["alice"]["0"], length=0.5, crypt=david.keys["bob"]["qkd"])
bob.check_incoming("part david alice 0", crypt=bob.keys["david"]["qkd"])
david.send_key_part("bob", david.keys["alice"]["1"], length=0.5, crypt=david.keys["bob"]["qkd"])
bob.check_incoming("part david alice 1", crypt=bob.keys["david"]["qkd"])
bob.send_key_part("david", david.keys["david"]["0"], length=0.5, crypt=bob.keys["david"]["qkd"])
david.check_incoming("part bob alice 0", crypt=david.keys["bob"]["qkd"])
bob.send_key_part("david", david.keys["david"]["1"], length=0.5, crypt=bob.keys["david"]["qkd"])
david.check_incoming("part bob alice 1", crypt=david.keys["bob"]["qkd"])

alice.send_data("bob", msg="1" +alice.keys["bob"]["1"]+alice.keys["david"]["1"])
alice.send_data("david", msg="1 "+alice.keys["bob"]["1"]+alice.keys["david"]["1"])

bob.receive_keys("alice")
bob_result=bob.verify_keys()

if bob_result:
    print("BOB VERIFIED THE KEYS")
else:
    print("BOB COULDN'T VERIFY THE KEYS")
    raise 

david.receive_keys("alice")
david_result=david.verify_keys()

if david_result:
    print("DAVID VERIFIED THE KEYS")
else:
    print("DAVID COULDN'T VERIFY THE KEYS")

if bob_result and david_result:
    print("THE PROCESS WAS SUCCESFUL")
