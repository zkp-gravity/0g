hash_functions_per_bloom_filter=2
discriminators=10
k=2**10
bloom_filters=56
input_value_bits=28
hash_digest_value_bits=hash_functions_per_bloom_filter*discriminators + 1 
bloom_filter_value_bits=discriminators*hash_functions_per_bloom_filter

code = f"program main.aleo;\n\n"

# NOTE: we need 7864320 table entries in total
# Amount of entries should be `discriminators` * `bloom_filters` * `k`, the values of entries could be random numbers for now
tableentrycounter = 0
for i in range(bloom_filters):
    for j in range(discriminators):
        code += f"""table bloomtable_{i}_{j}:
    input field;
    input field;
    input field; 
"""
        entries = k
        for entry in range(entries):
            tableentrycounter += 1
            code += f"    entry {tableentrycounter}field {tableentrycounter}field {tableentrycounter}field;\n"
        code += f"\n"

input_bits = "{" + f"\n"
hash_digest_bits = "{" + f"\n"
bloom_filter_bits = "{" + f"\n"

# input_bits structs
code += f"struct input_value:\n"
for i in range(input_value_bits):
    code += f"    bit{i} as field;\n"
code += f"\n"
code += f"struct input_bits:\n"
for i in range(bloom_filters):
    code += f"    in{i} as input_value;\n"
code += f"\n"
# input bit inputs
for i in range(bloom_filters):
    input_bits += f"    in{i}: " + "{" + f"\n"
    for j in range(input_value_bits):
        input_bits += f"        bit{j}: 1field,\n" if j < (input_value_bits - 1) else f"        bit{j}: 1field\n"
    input_bits += "    }," + f"\n" if i < (bloom_filters - 1) else "    }" + f"\n"

# hash_digest_bits structs
code += f"struct hash_digest_value:\n"
for i in range(hash_digest_value_bits):
    code += f"      bit{i} as field;\n"
code += f"\n"
code += f"struct hash_digest_bits:\n"
for i in range(bloom_filters):
    code += f"      in{i} as hash_digest_value;\n"
code += f"\n"
# hash_digest bit inputs
for i in range(bloom_filters):
    hash_digest_bits += f"    in{i}: " + "{" + f"\n"
    for j in range(hash_digest_value_bits):
        hash_digest_bits += f"        bit{j}: 1field,\n" if j < (hash_digest_value_bits - 1) else f"        bit{j}: 1field\n"
    hash_digest_bits += "    }," + f"\n" if i < (bloom_filters - 1) else "    }" + f"\n"

# bloom_filter_values structs
code += f"struct bloom_filter_value:\n"
for i in range(bloom_filter_value_bits):
    code += f"      bit{i} as field;\n"
code += f"\n"
code += f"struct bloom_filter_bits:\n"
for i in range(bloom_filters):
    code += f"      in{i} as bloom_filter_value;\n"
code += f"\n"
code += f"\n"
# bloom_filter bit inputs
for i in range(bloom_filters):
    bloom_filter_bits += f"    in{i}: " + "{" + f"\n"
    for j in range(bloom_filter_value_bits):
        bloom_filter_bits += f"        bit{j}: 1field,\n" if j < (bloom_filter_value_bits - 1) else f"        bit{j}: 1field\n"
    bloom_filter_bits += "    }," + f"\n" if i < (bloom_filters - 1) else "    }" + f"\n"


code += f"""
function main:
    input r0 as input_bits.private;
    input r1 as hash_digest_bits.private;
    input r2 as bloom_filter_bits.private;
"""

input_bits += "}"
hash_digest_bits += "}"
bloom_filter_bits += "}"

f = open("main.aleo", "w")
f.write(code)
f.close()

f = open("input_bits.txt", "w")
f.write(input_bits)
f.close()

f = open("hash_digest_bits.txt", "w")
f.write(hash_digest_bits)
f.close()

f = open("bloom_filter_bits.txt", "w")
f.write(bloom_filter_bits)
f.close()