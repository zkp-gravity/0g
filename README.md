![](zero-gravity-banner.png)

Zero Gravity is a system for proving an inference pass (i.e. a classification) for a pre-trained, public Weightless Neural Network run on a private input. Zero Gravity builds upon the recent BTHOWeN model by [Susskind et al (2022)](https://arxiv.org/abs/2203.01479), in which the authors improve upon earlier WNN models in a number of interesting ways.  Most importantly for this hackathon project, they helpfully provide an [implementation](https://github.com/ZSusskind/BTHOWeN) complete with pre-trained models and reproducible benchmarks.

See our [blog post](https://hackmd.io/@77sjNbqjST6HRnGPQyY9Dw/BkNGwbUW3) for an extensive description!

Built as part of the ZKHack hackathon, Lisbon, 2023.

## Setup

Clone and install the [custom aleo compiler](git@github.com:zkp-gravity/aleo-setup.git) supporting lookup arguments

## Usage
Values in the example below were generated using our fork of [BTHOWeN](https://github.com/zkp-gravity/BTHOWeN).
```
python3 scripts/generate_aleo_code.py 56
../aleo-setup/aleo/target/debug/aleo run main "$(cat input_file.txt)" "$(cat hash_values.txt)" "$(cat bloom_filters.txt)" $(cat winning_discriminator_value.txt) "$(cat winning_discriminator_index.txt)"
```

## Implementation notes and limitations
- All inputs are private, except for which discriminator (category) succeeded, as well as the model itself. 
- Proving time of e.g. a full MNIST example is not practical yet. PRs and suggestions for improvement are welcome.
- ❌ Print statements during the build phase are expected - and will be removed in future iterations of Aleo.
- The number of lookup constraints are not included in the final print statement but will show up when compiling in debug mode.
- Note that even when changing certain inputs, the proof might succeed, as it essentially checks which discriminator won. 