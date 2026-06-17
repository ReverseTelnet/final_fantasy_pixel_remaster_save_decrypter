

import sys
import zlib
import json
import base64
import hashlib
from pathlib import Path
from py3rijndael import RijndaelCbc
from py3rijndael import ZeroPadding



BLOCK_SIZE = 32
ITERATIONS = 10
PASSWORD   = 'TKX73OHHK1qMonoICbpVT0hIDGe7SkW0'
SALTWORD   = '71Ba2p0ULBGaE6oJ7TjCqwsls1jBKmRL'



def read_bytes(filename):
    with open(filename, 'rb') as f:
        return f.read()



def write_bytes(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)



def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)



def write_json(filename, data, pretty=False):
    with open(filename, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))



def make_directories():
    from os import makedirs
    makedirs('encrypted', exist_ok=True)
    makedirs('decrypted', exist_ok=True)



def make_cipher():
    '''Derive key + IV from PASSWORD/SALTWORD and return a configured cipher.'''
    derived = hashlib.pbkdf2_hmac('sha1', PASSWORD.encode(), SALTWORD.encode(), ITERATIONS, dklen=64)
    key, iv = derived[:32], derived[32:64]
    return RijndaelCbc(key, iv, padding=ZeroPadding(BLOCK_SIZE), block_size=BLOCK_SIZE)



def detect_format(data):
    '''
    Detect whether save data is PC (base64/UTF-8 BOM) or PS (raw binary).
        PC saves begin with a UTF-8 BOM (EF BB BF) or are valid ASCII/base64 text.
        PS saves are raw binary with no BOM and non-printable bytes.
        Returns 'pc' or 'ps'.
    '''
    # UTF-8 BOM 
    if data[:3] == b'\xef\xbb\xbf':
        return 'pc'
    # Try Decoding As Ascii
    try:
        text = data.decode('ascii').strip()
        # Check For Base64 Characters, Padding, And Whitespace
        import re
        if re.fullmatch(r'[A-Za-z0-9+/=\r\n]+', text):
            return 'pc'
    except (UnicodeDecodeError, ValueError):
        pass
    return 'ps'



def decrypt_binary(ciphertext):
    compressed = bytes(make_cipher().decrypt(ciphertext))
    return zlib.decompress(compressed, wbits=-15)



def decrypt_base64(encoded):
    '''Strip BOM, base64-decode, decrypt, and decompressed JSON bytes.'''
    if encoded[:3] == b'\xef\xbb\xbf':
        encoded = encoded[3:]
    return decrypt_binary(base64.b64decode(encoded))



def encrypt_to_binary(json_bytes):
    '''Compress and encrypt JSON bytes (Playstation Format)'''
    compressed = zlib.compress(json_bytes, wbits=-15)
    return bytes(make_cipher().encrypt(compressed))


def encrypt_to_base64(json_bytes):
    '''Compress and encrypt JSON bytes, base64-encoded ciphertext (PC Format)'''
    return base64.b64encode(encrypt_to_binary(json_bytes))



def load_save_file(filename):
    raw = read_bytes(filename)
    save_format = detect_format(raw)
    if save_format == 'pc':
        json_bytes = decrypt_base64(raw)
    else:
        json_bytes = decrypt_binary(raw)
    data = json.loads(json_bytes.decode('utf-8'))
    return data, save_format



def save_save_file(filename, data, platform='ps'):
    json_bytes = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if platform == 'pc':
        payload = b'\xef\xbb\xbf' + encrypt_to_base64(json_bytes) + b'\r\n'
    else:
        payload = encrypt_to_binary(json_bytes)
    write_bytes(filename, payload)
    return len(payload)



def decrypt_save_file(input_filename, output_filename=None):
    input_file = Path(input_filename)
    if output_filename is None:
        output_file = Path(f'decrypted/{input_file.stem}.json')
    else:
        output_file = Path(output_filename)
    data, save_format = load_save_file(input_file)
    print(f'Detected Format: {save_format.upper()}')
    write_json(output_file, data)
    size = len(json.dumps(data, separators=(',', ':')).encode('utf-8'))
    print(f'Decrypted To   : {output_file} ({size:,} bytes)')



def encrypt_save_file(input_filename, output_filename=None, platform='None'):
    input_file = Path(input_filename)
    platform = platform.lower()
    if platform not in ('pc', 'ps'):
        raise ValueError('Platform must be "pc" or "ps".')
    if output_filename is None:
        output_file = Path(f'encrypted/{input_file.stem}.sav') if platform == 'ps' else Path(f'encrypted/{input_file.stem}')
    else:
        output_file = Path(output_filename)
    data = read_json(input_file)
    size = save_save_file(output_file, data, platform)
    print(f'Platform:  {platform.upper()}')
    print(f'Encrypted: {output_file} ({size:,} bytes)')



if __name__ == '__main__':


    args = sys.argv[1:]
    command = args[0].lower()


    if command == 'decrypt':
        input_filename = args[1]
        output_filename = args[2] if len(args) > 2 else None
        decrypt_save_file(input_filename, output_filename)


    elif command == 'encrypt_pc':
        input_filename = args[1]
        output_filename = args[2] if len(args) > 2 else None
        platform = 'pc'
        encrypt_save_file(input_filename, output_filename, platform)


    elif command == 'encrypt_ps':
        input_filename = args[1]
        output_filename = args[2] if len(args) > 2 else None
        platform = 'ps'
        encrypt_save_file(input_filename, output_filename, platform)


