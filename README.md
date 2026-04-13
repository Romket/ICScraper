# ICScraper
Reverse engineered calls to Infinite Campus backend

## Limitations
ICScraper currently only does API calls to `UserAccount`, `Notification-retrieve`, `gpa`, and `grades`

## Installation

To install ICScraper, run the following commands:

```
git clone https://github.com/Romket/ICScraper.git
cd ICScraper
pip install requirements.txt
```

## Run

To run ICScraper:

1. Create a `.env` file that matches the formatting in [`sample.env`](sample.env) with your IC username and password.
2. Run the program using `python icscraper.py`.

## Output

ICScraper outputs all stored data to `out/`. Each `.json` file there represents the result of a different API call.