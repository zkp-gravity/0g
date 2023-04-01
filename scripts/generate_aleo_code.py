import sys

def main(xs):

    hash_functions_per_bloom_filter=2
    discriminators=10
    k=2**10
    bloom_filters=56 # len(xs)
    input_value_bits=28
    hash_digest_value_bits=hash_functions_per_bloom_filter*discriminators + 1 
    bloom_filter_values=hash_functions_per_bloom_filter
    n_hash_bits = hash_digest_value_bits
    bloom_filter_value_bits=hash_functions_per_bloom_filter*discriminators

    assert n_hash_bits == 21
    p = 2 ** n_hash_bits - 1

    hash_values = [(x * x * x) % p for x in xs]
    quotients = [(x * x * x) // p for x in xs]
    msbs = [
        0 if hash_value & (1 << (n_hash_bits - 1)) == 0 else 1
        for hash_value in hash_values
    ]
    index1s = [
        hash_value % (2 ** (n_hash_bits - 1)) >> 10
        for hash_value in hash_values
    ]
    index2s = [
        hash_value % (2 ** 10)
        for hash_value in hash_values
    ]

    with open("main.aleo", "w") as f:

        f.write(f"program main.aleo;\n\n")

        # Amount of entries should be `discriminators` * `bloom_filters` * `k`, the values of entries
        tableentrycounter = 0 # TODO: We need to import values from a program run
        tables = ""
        for i in range(bloom_filters):
            for j in range(discriminators):
                tables += f"""table bloomtable_{i}_{j}:
    input field;
    input field;
    input field;\n"""
                for entry in range(k):
                    tableentrycounter += 1 # [0,2**10]              [0,1]
                    tables += f"    entry {tableentrycounter}field {tableentrycounter}field 0field;\n"
                tables += f"\n"
        f.write(tables)

        f.write("\n")
        f.write(f"struct Inputs:\n")
        for i in range(len(xs)):
            f.write(f"    in{i} as field;\n")
        f.write("\n")

        f.write("\n")
        f.write(f"struct HashBits:\n")
        f.write(f"    index1 as field;\n")
        f.write(f"    index2 as field;\n")
        f.write(f"    msb as field;\n")
        f.write("\n")

        f.write("\n")
        f.write(f"struct HashInfo:\n")
        f.write(f"    decomposition as HashBits;\n")
        f.write(f"    hash as field;\n")
        f.write(f"    quotient as field;\n")
        f.write("\n")

        f.write("\n")
        f.write(f"struct HashInfos:\n")
        for i in range(len(xs)):
            f.write(f"    info{i} as HashInfo;\n")
        f.write("\n")

        # bloom_filter_values structs
        bloom_filter_bits_str = f"struct BloomFilterValue:\n"
        for i in range(bloom_filter_value_bits):
            bloom_filter_bits_str += f"      bit{i} as field;\n"
        bloom_filter_bits_str += f"\n"
        bloom_filter_bits_str += f"struct BloomFilterBits:\n"
        for i in range(bloom_filters):
            bloom_filter_bits_str += f"      in{i} as BloomFilterValue;\n"
        bloom_filter_bits_str += f"\n"
        f.write(bloom_filter_bits_str)

        f.write(f"closure validate_hash:\n")
        f.write("    // The input x\n")
        f.write("    input r0 as field;\n")
        f.write("    // The claimed hash\n")
        f.write("    input r1 as field;\n")
        f.write("    // The quotient x^3 // p\n")
        f.write("    input r2 as field;\n")
        f.write("    // Compute x^3, put into r4\n")
        f.write(f"    mul r0 r0 into r3;\n")
        f.write(f"    mul r0 r3 into r4;\n")
        f.write("    // Compute quotient * p + claimed hash, put into r6\n")
        f.write(f"    mul r2 {p}field into r5;\n")
        f.write(f"    add r5 r1 into r6;\n")
        f.write("    // Assert both are equal\n")
        f.write(f"    assert.eq r4 r6;\n")
        f.write("\n")

        f.write(f"closure validate_bit_decomposition:\n")

        f.write("    input r0 as field;\n")
        f.write(f"    input r1 as HashBits;\n")
        f.write("\n")


        f.write("    // We don't have to validate that the indices are 10-bit integers, because\n")
        f.write("    // we'll use them in table lookups later!\n")

        f.write("    // Validate bit constraint on MSB\n")
        f.write(f"    sub 1field r1.msb into r2;\n")
        f.write(f"    mul r1.msb r2 into r3;\n")
        f.write(f"    assert.eq 0field r3;\n")
        f.write("\n")

        f.write("    // Recompute x\n")
        f.write(f"    mul r1.msb {1 << 10}field into r4;\n")
        f.write(f"    add r4 r1.index1 into r5;\n")
        f.write(f"    mul r5 {1 << 10}field into r6;\n")
        f.write(f"    add r6 r1.index2 into r7;\n")

        f.write("\n")
        f.write("    // Assert recomputed value equals first argument\n")
        f.write(f"    assert.eq r0 r7;\n")

        f.write("\n")
        f.write("function main:\n")
        f.write(f"    input r0 as Inputs.private;\n")
        f.write(f"    input r1 as HashInfos.private;\n")
        f.write(f"    input r2 as BloomFilterBits.private;\n")
        for i in range(bloom_filters):
            f.write(f"\n    call validate_hash r0.in{i} r1.info{i}.hash r1.info{i}.quotient;\n")
            f.write(f"    call validate_bit_decomposition r1.info{i}.hash r1.info{i}.decomposition;\n")
            for j in range(discriminators):
                f.write(f"    lookup bloomtable_{i}_{j} r1.info{i}.decomposition.index1 r2.in{i}.bit{j} 0field;\n")
                f.write(f"    lookup bloomtable_{i}_{j} r1.info{i}.decomposition.index2 r2.in{i}.bit{10+j} 0field;\n")
    
    with open("inputs.txt", "w") as f:
        fields_string = ", ".join([f"in{i}: {x}field" for i, x in enumerate(xs)])
        f.write("{" + fields_string + "}")

    with open("hash_bits.txt", "w") as f:
        fields_string = ", ".join([
            f"info{i}: " + "{" + 
                "decomposition: " +
                "{" +
                    f"index1: {index1s[i]}field, index2: {index2s[i]}field, msb: {msbs[i]}field"
                "}, " +
                f"hash: {hash_values[i]}field, quotient: {quotients[i]}field" +
            "}"
            for i in range(n_inputs)
        ])
        f.write("{" + fields_string + "}")

if __name__ == "__main__":
    n_inputs = int(sys.argv[1])
    xs = list(range(n_inputs))
    main(xs)