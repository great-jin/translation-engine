# Translation Engine
Translation Engine is for Daily Word project, provide translate ability through API.

## Model
The engine model base on [Meta NLLB](https://ai.meta.com/research/no-language-left-behind/).


## Install
To start with, you need download model first.

Choose the corresponding model according to your needs, the greater the model parameters, the better the effect, and the higher the requirements for the server. 

- [nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M/tree/main)
- [nllb-200-distilled-1.3B](https://huggingface.co/facebook/nllb-200-distilled-1.3B/tree/main)
- [nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B/tree/main)
- [nllb-200-3.3B](https://huggingface.co/facebook/nllb-200-3.3B/tree/main)

Download the following files:

- config.json
- generation_config.json
- pytorch_model.bin
- sentencepiece.bpe.model
- special_tokens_map.json
- tokenizer.json
- tokenizer_config.json

After model is installed, rewrite model to ct2, optional: `int8`, `int8_float16`, `int8_bfloat16`, `int16`, `float16`, `float32`.

Normally, base on CPU mode recommend set to `int8`, if CPU supported `FP16`, `BF16` then can choose `int8_float16` or `int8_bfloat16`. 

If base on GPU then `float16` would achieve a good balance.
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

Start and stop the background service using the following commands.
```bash
# star server
nohup /usr/local/python311/bin/uvicorn main:app --host 0.0.0.0 --port 8080 > uvicorn.log 2>&1 &

# stop server
ps aux | grep uvicorn
kill -9 <PID>
```

**Notice:** If you want to deploy to a server, make sure the machine memory is great then `4G` to load nllb model.