program main.aleo;

table triple:
    input field;
    input field;
    input field;
    entry 1field 1field 1field;
    entry 1field 2field 3field;

function main:
    input r0 as field.private;
    input r1 as field.private;
    input r2 as field.private;
    lookup triple r0 r1 r2;

