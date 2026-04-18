import certifi
import os

import warnings
warnings.filterwarnings("ignore", message=".*charset_normalizer.*")

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()