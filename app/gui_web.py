import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from components.component import Component
from app.estimator_engine import EstimatorEngine

engine = EstimatorEngine()

st.title("Drone Tooling Cost Estimator")

# Initialize session state
if "components" not in st.session_state:
    st.session_state.components = []

# -----------------------------
# Component Input
# -----------------------------

st.header("Add Component")

name = st.text_input("Component name")

length = st.number_input("Length (mm)", value=1000)
width = st.number_input("Width (mm)", value=200)
thickness = st.number_input("Thickness (mm)", value=50)

if st.button("Add Component"):

    comp = Component(name, length, width, thickness)

    st.session_state.components.append(comp)

# -----------------------------
# Show Component List
# -----------------------------

st.header("Current Components")

if len(st.session_state.components) == 0:
    st.write("No components added yet.")

for c in st.session_state.components:
    st.write(f"{c.name} | L:{c.length} W:{c.width} T:{c.thickness}")

# -----------------------------
# Calculation
# -----------------------------

if st.button("Calculate Cost"):

    total = 0

    st.header("Results")

    for comp in st.session_state.components:

        result = engine.process_component(comp)

        st.write(
            f"{comp.name} → €{result['component_cost']}"
        )

        total += result["component_cost"]

    st.subheader(f"Total Project Cost: €{total}")

# -----------------------------
# Clear Project
# -----------------------------

st.divider()

if st.button("Start New Project"):

    st.session_state.components = []

    st.rerun()