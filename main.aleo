program main.aleo;

// NOTE: number of inputs depends on number of hash functions we use
closure and_values:
    input r0 as field;
    input r1 as field;
    input r2 as field;
    input r3 as field;
    
    mul r1 r2 into r4;
    mul r3 r4 into r5;
    mul r4 r5 into r6;

    output r6 as field;

table bloomtable:
    input field;
    input field;
    input field;
    entry 1field 2field 5field;
    entry 4field 5field 6field;
    entry 7field 8field 9field;
    entry 10field 11field 12field;

struct table_entry:
    a0 as field; // 5 bits
    a1 as field; // 5 bits
    a2 as field; // 13 bits
    a3 as field; // 1 bit
    a4 as field; // Max_Value

function main:
    input r0 as table_entry.private;

    mul r0.a2 2field into r1;
    add r0.a3 r1 into r2;
    lookup bloomtable r0.a0 r0.a2 r2;

    call and_values r0.a3 r0.a3 r0.a3 r0.a3 into r3;

    // summation proof
    // NOTE: can perhaps be done with a lookup
    add r3 r3 into r4;
    add r4 r4 into r5;

    // argmax proof
    // NOTE: first part can be done with a lookup
    // part a)
    gt r0.a3 r0.a3 into r6;
    ternary r6 r0.a3 r0.a3 into r7;
    assert.eq r0.a4 r7;

