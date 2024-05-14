#!/home/ubuntu/bin/miniconda3/envs/oi/bin/python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv

# Uncomment the following line and populate the file '_private/api_keys.env' with the requisite API keys,
# if there is a need to access other systems (such as OpenAI's LLMs).
#load_dotenv('_private/api_keys.env')

import os 
import re
import sys
from interpreter.terminal_interface.start_terminal_interface import main
#import interpreter.terminal_interface.start_terminal_interface

if __name__ == '__main__':

    TEMPERATURE = 0.0

#    model = 'gpt'
#    model = 'hf'
#    model = 'claude3'
    model = 'lmstudio'

    args2 = []
    if model=='claude3':
        MODEL_API_KEY_NAME = 'ANTHROPIC_API_KEY'
        MODEL_NAME = 'claude-3-opus-20240229'
#       MODEL_NAME = 'claude-3-sonnet-20240229'
        api_key = os.getenv(MODEL_API_KEY_NAME)
    elif model=='gpt':
        MODEL_API_KEY_NAME = 'OPENAI_API_KEY_OI'
        MODEL_NAME = 'gpt-3.5-turbo'
    #     MODEL_NAME = 'gpt-4'
        api_key = os.getenv(MODEL_API_KEY_NAME)
    elif model=='hf':
        MODEL_API_KEY_NAME = 'HF_HUB'
    # #    MODEL_NAME = 'huggingface/gradientai/Llama-3-70B-Instruct-Gradient-1048k'
        MODEL_NAME = 'gradientai/Llama-3-8B-Instruct-Gradient-1048k'
        api_key = os.getenv(MODEL_API_KEY_NAME)
        args2 = [
            '--api_base', f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
#        '--api_type', 'huggingface'
#        '--api_base', f'https://huggingface.co/inference-endpoints/{MODEL_NAME}'
        ]
        # OpenAIException - Error code: 404 - {'error': 'Model gradientai/Llama-3-8B-Instruct-Gradient-1048k/chat/completions does not exist'}
    elif model=='lmstudio':
        args2 = [
            '--api_base', "http://192.168.1.246:1234/v1"
        ]
        api_key = "lm-studio"
        MODEL_NAME = 'lm-studio'

    args = [
        '--temperature', f'{TEMPERATURE}',
        '--api_key', f'{api_key}',
        '--model', MODEL_NAME,
        '--os',
    #    '--disable_telemetry',
#        '--profile', 
    ]
    sys.argv.extend(args)
    sys.argv.extend(args2)

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
