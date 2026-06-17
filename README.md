# Final Fantasy Pixel Remaster Save Encrypt and Decrypt Tool

This repository Encrypts and Decrypts Final Fantasy Pixel Remaster Save Files. <br>
Both Playstation 4 and PC Save Games are supported, and the decryption logic automatically detects the format. <br>

## Decryption Logic

### Playstation Decryption

- Decrypt
- DEFLATE-decompress
- Save as JSON

### PC Decryption

- Strip BOM
- Base64 Decode
- Decrypt
- DEFLATE-decompress
- Save as JSON

### Pretty JSON

See [Final Fantasy Pixel Remaster Save JSON Pretty](https://github.com/ReverseTelnet/final_fantasy_pixel_remaster_save_json_pretty) for methods to wrap and unwrap the deeply nested JSON-in-a-string-in-a-string. <br>

## Encryption Logic

### Playstation Encryption

- DEFLATE-compress JSON FIle
- Encrypt
- Base64 Encode

### PC Encryption

- DEFLATE-compress JSON FIle
- Encrypt
- Base64 Encode
- Save as Binary with BOM and CRLF `\r\n`

## How to Use

Storage is cheap, starting over is not. <br>
Always have a backup of your file. <br>

## Decrypt Save Files

If an output filename is not provided, files are written to the `decrypted` folder. <br>
The extension `.json` is added to the original filename. <br>

```shell
python ff_pr_save_tool.py decrypt <input_save> [output.json]
```

### Decrypt Examples

```shell
python ff_pr_save_tool.py decrypt samples/ff1_pr/encrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk=
Detected Format: PC
Decrypted To   : decrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk=.json (149,953 bytes)
```

```shell
python ff_pr_save_tool.py decrypt samples/ff6_pr/encrypted/slot8.sav
Detected Format: PS
Decrypted To   : decrypted/slot8.json (348,271 bytes)
```

```shell
python ff_pr_save_tool.py decrypt samples/ff6_pr/encrypted/slot10.sav decrypted/slot_10_decrypt.json
Detected Format: PS
Decrypted To   : decrypted/slot_10_decrypt.json (477,630 bytes)
```

## Encrypt Save Files

If an output filename is not provided, files are written to the `encrypted` folder. <br>
The extension `.sav` is added to the original filename when using the `encrypt_ps` method. <br>
No extension `.sav` is added to the original filename when using the `encrypt_pc` method. <br>

- `encrypt_pc` = PC Format
- `encrypt_ps` = Playstation Format

```shell
python ff_pr_save_tool.py encrypt_pc <input.json> [output_save]
python ff_pr_save_tool.py encrypt_ps <input.json> [output_save]
```

### Encrypt Examples

```shell
python ff_pr_save_tool.py encrypt_pc decrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk=.json
Platform:  PC
Encrypted: encrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk= (83,973 bytes)
```

```shell
python ff_pr_save_tool.py encrypt_ps decrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk=.json
Platform:  PS
Encrypted: encrypted/Rl18osV3e9kPX9SMWQj8mqShFpTUmu1lf6Mb=FVVfqk=.sav (62,976 bytes)
```

```shell
python ff_pr_save_tool.py encrypt_pc decrypted/slot_10_decrypt.json
Platform:  PC
Encrypted: encrypted/slot_10_decrypt (52,273 bytes)
```

```shell
python ff_pr_save_tool.py encrypt_ps decrypted/slot_10_decrypt.json encrypted/slot_10.sav
Platform:  PS
Encrypted: encrypted/slot_10.sav (39,200 bytes)
```

## Related Implementations and Inspiration

This repository borrowed heavily from the encoding logic and encryption methods documented and released in these repositories:
It is based on the work done by:

- [bucanero's Save Decrypters](https://github.com/bucanero/save-decrypters/tree/master/ff-pixel-decrypter) (C)
- [Anub1sR0cks](https://github.com/Anub1sR0cks/FFPRSaveEditor) (C#)
- [KiameV](https://github.com/KiameV/final-fantasy-pr-save-editor) (Go)
