

## requirements

- Python 3.x
- colorama

dependance:

```bash
pip install colorama
```

## utilisation

```bash
python main.py [OPTIONS] [HOST]

# Scan with a URL (recommended)
python main.py -S https://example.com

# Scan avec hostname
python main.py example.com

# Scan une rangée de ports
python main.py -S https://example.com -s 1 -e 100

# Scan ports specifiques
python main.py -S https://example.com -P 21,22,80,443

# Combine: ports custom avec hostname
python main.py example.com -P 80,443,8080
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-S, --site` | Target URL (e.g. `https://example.com`) | |
| `HOST` | Target host name (positional fallback) | |
| `-s, --start` | Start port for range scan | 1 |
| `-e, --end` | End port for range scan | 1025 |
| `-P, --ports` | Comma-separated specific ports to scan | |

## Output

- **Green `[OPEN]`** ports ouverts
- **Gray `[CLOSED]`** ports closed
