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

function main:
    input r0 as field.private; // 5 bits
    input r1 as field.private; // 5 bits
    input r2 as field.private; // 13 bits
    input r3 as field.private; // 1 bit
    input r4 as field.private; // Max_Value

    mul r2 2field into r5;
    add r3 r5 into r6;
    lookup bloomtable r0 r2 r6;

    call and_values r3 r3 r3 r3 into r7;

    // summation proof
    // NOTE: can perhaps be done with a lookup
    add r7 r7 into r8;
    add r8 r8 into r9;

    // argmax proof
    // NOTE: first part can be done with a lookup
    // part a)
    gt r3 r3 into r10;
    ternary r10 r3 r3 into r11;
    assert.eq r4 r11;

