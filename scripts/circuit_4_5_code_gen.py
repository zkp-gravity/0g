def generate_code(h=4, B=20, D=20, k=13):
    code = """
program main.aleo;

table bloomtable:
    input field;
    input field;
    input field; 
    // Amount of entries should be `D` * `B` * `k`, the values of entries could be random numbers for now
"""
    entries = D * B * k
    for i in range(entries):
        code += f"    entry {i + 1}field {i + 2}field {i + 3}field;\n"

    code += """
// number of inputs values depends on number of hash functions `h` we use
closure and_values:
"""
    for i in range(h):
        code += f"    input value{i + 1} as field;\n"

    tmp_values = []
    for i in range(h - 1):
        tmp_values.append(f"tmp{i}")
        code += f"    mul value{i + 1} value{i + 2 if i + 2 <= h else 1} into {tmp_values[i]};\n"

    code += f"    output {tmp_values[-1]} as field;\n"

    code += """
closure lookup_check:
    input bloom_filter_index  as field.private; // log(`B`) bits
    input discriminator_index as field.private; // log(`D`) bits
    input hash_digest        as field.private; // `k` bits
    input value               as field.private; // 1 bit

    mul hash_digest 2field into hash_digest_shifted;
    add value hash_digest_shifted into value_hash_digest;
    lookup bloomtable bloom_filter_index discriminator_index value_hash_digest;

function main:
"""
    for i in range(D):
        code += f"    input discriminator_{i + 1} as field.private;\n"
    for i in range(B):
        code += f"    input bloom_filter_{i + 1} as field.private;\n"
    for i in range(B):
        for j in range(h):
            code += f"    input hash_digest_{i + 1}_{j + 1} as field.private;\n"
    for i in range(B):
        for j in range(h):
            for s in range(D):
                code += f"    input lookup_value_{i + 1}_{j + 1}_{s + 1} as field.private;\n"

    for i in range(B):
        for s in range(D):
            tmp_values = []
            for j in range(h):
                tmp_values.append(f"lookup_value_{i + 1}_{j + 1}_{s + 1}")
            code += f"    call and_values {' '.join(tmp_values)};\n"
    
    return code
print(generate_code(4, 2, 2, 13))