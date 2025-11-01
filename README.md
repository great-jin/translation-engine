# Translation Engine
Translation Engine is for Daily Word project, provide translate ability through API.

## Model
The engine model base on [facebook nllb](https://huggingface.co/facebook/nllb-200-distilled-600M/).


## Install
To start with, you need download model first.

Visit the website of [nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main), download the following files.

- config.json
- generation_config.json
- pytorch_model.bin
- sentencepiece.bpe.model
- special_tokens_map.json
- tokenizer.json
- tokenizer_config.json

After model is installed, rewrite model to ct2, optional: `int8`, `int16`, `float16`, `float32`.
```bash
ct2-transformers-converter \
    --model <path_to_nllb_file> \
    --output_dir <output_dir> \
    --quantization int8
```

After model is converted, then update the `config/application.yml` file.

Then execute the following command to install required package, and you free to go.
```bash
pip install -r requirements.txt
```

**Notice:** If you want to deploy to a server, make sure the machine memory is great then `4G` to load nllb model.