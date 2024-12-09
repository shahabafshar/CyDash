# **CyDash: Cyber Events Interactive Dashboard**

Welcome to CyDash, an interactive dashboard designed to analyze and visualize cybersecurity events. CyDash enables security researchers, analysts, and organizations to explore trends, correlations, and insights using an intuitive, filterable interface. The dashboard is powered by Python, Dash, and Plotly, making it both powerful and extensible.

[![CyDash Intro Video](https://img.youtube.com/vi/Q4djFfN35mA/0.jpg)](https://youtu.be/Q4djFfN35mA)

---

## **Features**

- **Interactive Visualizations**: Includes bar charts, pie charts, heatmaps, and choropleth maps for in-depth analysis.
- **Dynamic Filtering**: Filter data by year, actor type, country, industry, and more.
- **Slicing**: Click on visual elements to dynamically adjust filters and refine your analysis.
- **Responsive Design**: Works seamlessly on different devices with Bootstrap-based layouts.
- **Customizable**: Easily modify the filters and visualizations via `config.json` without changing the source code.

---

## **Getting Started**

Follow these steps to set up and run CyDash on your local machine:

### **1. Prerequisites**

Ensure you have the following installed:
- Python 3.9 or later
- A text editor or IDE (e.g., VS Code, PyCharm)
- A terminal or command prompt for executing commands

---

### **2. Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shahabafshar/CyDash.git
   cd CyDash
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the Data**:
   Place the `Cyber Events Database - Records thru June 2024.xlsx` file in the project directory. This file is sourced from the [Center for International and Security Studies at Maryland (CISSM)](https://cissm.umd.edu/cyber-events-database).

---

### **3. Configuration**

The dashboard is highly configurable using `config.json`. This file defines the filters, visualizations, and layout. Modify it to add or remove filters and visualizations as needed.

---

### **4. Running the Application**

Run the application using the following command:
```bash
python CyDash.py
```

Once the server is running, open your browser and navigate to `http://127.0.0.1:8050`.

---

## **Usage**

1. **Filters**:
   Use the collapsible sidebar to select filters for year, actor type, country, industry, and more.
   
2. **Interactivity**:
   - Click on visual elements (e.g., bars, pie slices, heatmap cells) to dynamically slice data and refine your analysis.
   - Reset filters using the "Reset Filters" button in the sidebar.

3. **Visualizations**:
   - Analyze temporal trends, actor-specific patterns, and geographic impacts.
   - Gain actionable insights into targeted industries and common attack types.

---

## **File Structure**

```
CyDash/
├── CyDash.py                 # Main Python file for the dashboard
├── config.json               # Configuration file for filters and visualizations
├── requirements.txt          # List of required Python libraries
├── static/
│   └── css/
│       └── style.css         # Custom CSS for styling
├── Cyber Events Database.xlsx # Data source (to be added by the user)
└── README.md                 # Project documentation
```

---

## **Customization**

1. **Modify Filters**:
   Edit the `filters` section in `config.json` to add, remove, or change filter options.

2. **Add New Visualizations**:
   Add new items to the `visualizations` section in `config.json` with the appropriate chart type, columns, and layout properties.

3. **Styling**:
   Update `static/css/style.css` to change the appearance of dropdowns, charts, and layout components.

---

## **Data Source**

The data used for this dashboard is sourced from the [Center for International and Security Studies at Maryland (CISSM)](https://cissm.umd.edu/cyber-events-database). This dataset was selected for its comprehensive and structured information on cybersecurity events.

---

## **Dependencies**

- **Dash**: For building the interactive dashboard.
- **Dash Bootstrap Components**: For responsive design.
- **Plotly**: For creating advanced visualizations.
- **Pandas**: For data manipulation and preprocessing.
- **openpyxl**: For reading Excel files.

---

## **Contributing**

Contributions to CyDash are welcome! If you encounter issues, have feature requests, or would like to contribute enhancements, feel free to:
- Open an issue on the GitHub repository.
- Submit a pull request with detailed explanations of your changes.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## **Acknowledgments**

Special thanks to:
- [CISSM](https://cissm.umd.edu/) for providing the data.
- The Dash and Plotly communities for their powerful tools and libraries.

---

## **Contact**

For questions, suggestions, or feedback, please contact me at:
- Email: [shahab.afshar@outlook.com](mailto:shahab.afshar@outlook.com)
- Email: [safshar@iastate.edu](mailto:safshar@iastate.edu)

---

By following this guide, you'll have CyDash up and running, ready to deliver actionable insights into cybersecurity events!
