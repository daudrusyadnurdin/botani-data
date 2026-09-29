"""
Dashboard Dash pertama - Botani Data
Data: data/kebun.csv
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ===== 1. Load data =====
df = pd.read_csv("data/kebun.csv")
df["tanggal"] = pd.to_datetime(df["tanggal"])

# ===== 2. Inisialisasi app =====
app = Dash(__name__)

# ===== 3. Layout =====
app.layout = html.Div([
    html.H1("🌱 Dashboard Botani Data", style={"textAlign": "center"}),
    html.P("Dashboard pertama dengan Dash", style={"textAlign": "center", "color": "gray"}),
    
    html.Hr(),
    
    # Dropdown pilih tanaman
    html.Label("Pilih tanaman:"),
    dcc.Dropdown(
        id="dropdown-tanaman",
        options=[{"label": t, "value": t} for t in df["tanaman"].unique()],
        value=df["tanaman"].unique()[0],
        clearable=False,
    ),
    
    # Grafik
    dcc.Graph(id="grafik-tinggi"),
    
    html.Hr(),
    
    # Info ringkas
    html.Div(id="info-ringkas"),
])

# ===== 4. Callback =====
@app.callback(
    Output("grafik-tinggi", "figure"),
    Output("info-ringkas", "children"),
    Input("dropdown-tanaman", "value"),
)
def update_grafik(tanaman_pilihan):
    # Filter data
    dff = df[df["tanaman"] == tanaman_pilihan]
    
    # Bikin grafik
    fig = px.line(
        dff,
        x="tanggal",
        y="tinggi_cm",
        title=f"Pertumbuhan {tanaman_pilihan}",
        markers=True,
    )
    fig.update_layout(
        xaxis_title="Tanggal",
        yaxis_title="Tinggi (cm)",
    )
    
    # Info ringkas
    tinggi_awal = dff["tinggi_cm"].iloc[0]
    tinggi_akhir = dff["tinggi_cm"].iloc[-1]
    pertumbuhan = tinggi_akhir - tinggi_awal
    info = html.Div([
        html.H3("📊 Info Ringkas"),
        html.P(f"Tanaman: {tanaman_pilihan}"),
        html.P(f"Tinggi awal: {tinggi_awal} cm"),
        html.P(f"Tinggi akhir: {tinggi_akhir} cm"),
        html.P(f"Pertumbuhan: {pertumbuhan:.1f} cm"),
    ])
    
    return fig, info

# ===== 5. Run =====
if __name__ == "__main__":
    app.run(debug=True)