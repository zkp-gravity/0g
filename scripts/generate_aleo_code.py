import sys

def main(x, n_bits):
    bits = [
        0 if x & (1 << i) == 0 else 1
        for i in range(n_bits)
    ]

    print("program leotest.aleo;")

    fn_name = f"validate_bit_decomposition_{len(bits)}"
    # print(f"closure {fn_name}:")
    print("function main:")

    print("    // the hash")
    print("    input r0 as field.private;")

    print("    // Bits")
    for i in range(len(bits)):
        print(f"    input r{i + 1} as field.private;")

    r = len(bits) + 1

    print("    // Validate bit constraints")
    for i in range(len(bits)):
        print(f"    sub 1field r{i + 1} into r{r};")
        print(f"    mul r{i + 1} r{r} into r{r + 1};")
        print(f"    assert.eq 0field r{r + 1};")
        r += 2

    print("    // Recompute x")
    print(f"    mul r1 1field into r{r};")
    r += 1
    for i in range(1, len(bits)):
        print(f"    mul r{i + 1} {1 << i}field into r{r};")
        print(f"    add r{r - 1} r{r} into r{r + 1};")
        r += 2
    print(f"    assert.eq r0 r{r - 1};")

    # print()
    # print("function main:")
    # print("    // the hash")
    # print("    input r0 as field.public;")

    # print("    // Bits")
    # for i in range(len(bits)):
    #     print(f"    input r{i + 1} as field.public;")

    # parameter_string = " ".join([f"r{i}" for i in range(len(bits) + 1)])
    # print(f"    call {fn_name} {parameter_string};")

if __name__ == "__main__":
    x = int(sys.argv[1])
    n_bits = int(sys.argv[2])
    main(5, n_bits)