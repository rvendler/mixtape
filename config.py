# Application Configuration
import os
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, '.env')
load_dotenv(ENV_PATH)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENAI_ORG = os.environ.get('OPENAI_ORG')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
LLAMAAI_API_KEY = os.environ.get('LLAMAAI_API_KEY')

DEFAULT_MODEL = "openrouter-google/gemini-2.5-flash"
#DEFAULT_MODEL = "openrouter-anthropic/claude-sonnet-4"
#DEFAULT_MODEL = "openrouter-openai/o3-2025-04-16"
#DEFAULT_MODEL = "openrouter-meta-llama/llama-4-maverick"
#DEFAULT_MODEL = "openrouter-openai/gpt-4o-2024-11-20"
#DEFAULT_MODEL = "openrouter-google/gemini-2.5-pro"

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_REGION = os.environ.get('S3_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

REPLICATE_API_TOKEN = os.environ.get('REPLICATE_API_TOKEN')

SUNO_API_KEY = os.environ.get('SUNO_API_KEY')
