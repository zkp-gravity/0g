# 0g
![](zero-gravity-banner.png)

Zero-knowledge weightless machine learning

## Setup

Clone and install the [custom aleo compiler](git@github.com:zkp-gravity/aleo-setup.git) supporting lookup arguments

## Usage
```
python3 generate_main.py
../aleo-setup/aleo/target/debug/aleo run main "$(cat input_bits.txt)" "$(cat hash_digest_bits.txt)" "$(cat bloom_filter_bits.txt)" 
```

```
python3 generate_aleo_code.py 56
../aleo-setup/aleo/target/debug/aleo run main "$(cat inputs.txt)" "$(cat hash_bits.txt)" "$(cat inputs/bloom_filter_bits.txt)" $(cat max_discriminator.txt) "$(cat max_discriminator_index.txt)"
```
