# Dash Application

This was written to get a better understanding of Dash which combines a few different toolings.
The data is publicly available from the London Metal Exchange rate for the price per oz of the different metals.

### App structure
Currently it is all self contained in a single app.py
The next steps are to break it out so that has better overall structure and for now the structure is there but in the gitignore.
```
my_dash_app/
│
├── app.py               # Main entry point, handles initialization, layout, and routing
├── callbacks.py         # All app callbacks
├── assets/              # Static assets (CSS, images, etc.)
├── pages/               # Directory for page layouts
│   ├── home.py          # Layout and callbacks for the Home page
│   └── about.py         # Layout and callbacks for the About page
└── data/                # Directory for any data files
    └── metals.csv       # CSV data

```