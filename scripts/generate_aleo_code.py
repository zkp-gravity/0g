import sys

def main(xs, n_hash_bits):

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

        f.write("program main.aleo;\n")

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

#         f.write("""
# struct BloomLookupBits:
#     bit0 as field;
#     bit1 as field;
#     bit2 as field;
#     bit3 as field;

# """)
                
#         f.write("\n")
#         f.write(f"struct DiscriminatorBloomLookupBits:\n")
#         for i in range(len(xs)):
#             f.write(f"    lookup_bits{i} as BloomLookupBits;\n")
#         f.write("\n")


#         f.write("""
# struct AllBloomLookupBits:
#     class_0_bits as DiscriminatorBloomLookupBits;
#     class_1_bits as DiscriminatorBloomLookupBits;
#     class_2_bits as DiscriminatorBloomLookupBits;
#     class_3_bits as DiscriminatorBloomLookupBits;
#     class_4_bits as DiscriminatorBloomLookupBits;
#     class_5_bits as DiscriminatorBloomLookupBits;
#     class_6_bits as DiscriminatorBloomLookupBits;
#     class_7_bits as DiscriminatorBloomLookupBits;
#     class_8_bits as DiscriminatorBloomLookupBits;
#     class_9_bits as DiscriminatorBloomLookupBits;

# """)

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
        f.write("    input r0 as Inputs.private;\n")
        f.write(f"    input r1 as HashInfos.private;\n")
        for i in range(len(xs)):
            f.write(f"\n    call validate_hash r0.in{i} r1.info{i}.hash r1.info{i}.quotient;\n")
            f.write(f"    call validate_bit_decomposition r1.info{i}.hash r1.info{i}.decomposition;\n")
    
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
    n_hash_bits = int(sys.argv[1])
    n_inputs = int(sys.argv[2])
    xs = list(range(n_inputs))
    main(xs, n_hash_bits)