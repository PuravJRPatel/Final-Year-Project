# Final-Year-Project
Climate Modeling using Graphical Neural Networks.

## Phase: 1
1. Introduction: background,Problem statement, Objectives.
2. Literature survey: survey of  various implemented methodologies( at least 10 papers), gap analysis, performance parameters.
3. Proposed Methodology: Dataset summary, Block diagram, Flow diagram, Mathematical formulas and model.
4. Performance analysis of 30% project implemented.
5. Conclusions.

├── data/                   
│   ├── shapefile/            # Store the grid shapefile 
│   ├── rainfall/             # Store raw rainfall .nc files
│   ├── processed/            # Store processed CSVs with rainfall mapped to grid
│   ├── temperature/          # (Later) Store temperature .nc files
│   ├── final_graph/          # Store final graph dataset
│   └── grid_with_rainfall.csv # Final mapped rainfall data for nodes
│
├── scripts/                  
│   ├── grid_creation.py      # Generates the grid shapefile
│   ├── rainfall_mapping.py   # Maps rainfall data to grid nodes
│   ├── temperature_mapping.py # (Later) Maps temperature to grid
│   ├── graph_construction.py # Creates graph from nodes & edges
│   ├── visualization.py      # Plot results (optional)
│   └── train_gnn.py          # Train GNN model (later step)
│
├── notebooks/                # Jupyter notebooks for analysis
│   ├── exploratory_analysis.ipynb  # Initial EDA and visualization
│   ├── rainfall_mapping.ipynb      # Checking rainfall mapping
│   └── model_training.ipynb        # Training and evaluation
│
├── models/                   # Save trained GNN models
│   ├── checkpoints/          # Model checkpoints
│   ├── final_model.pth       # Final saved model
│   └── model_logs/           # Training logs and metrics
│
├── results/                  
│   ├── graphs/               # Visualizations (heatmaps, plots, etc.)
│   ├── evaluation_metrics/   # Performance results
│   └── predictions/          # Model predictions
│
├── main.py                   # Main script to run everything
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── .gitignore                 # Ignore unnecessary files (e.g., .nc, large raw data)