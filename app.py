import streamlit as st
import numpy as np
from simulation import ProjectileSimulator
import plotly.graph_objects as go
from PIL import Image
import os

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Projectile Dynamics Lab | Tarang Fest",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Main Styles */
    .main-header {
        font-size: 2.8rem !important;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.5rem;
        padding: 10px 0;
    }
    
    .sub-header {
        text-align: center;
        color: #4B5563;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        padding-bottom: 15px;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E5E7EB;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 5px;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Progress Bars */
    .progress-container {
        background: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #F3F4F6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid #E5E7EB;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3B82F6 !important;
        color: white !important;
    }
    
    /* Info Boxes */
    .info-box {
        background: #EFF6FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin: 15px 0;
    }
    
    .warning-box {
        background: #FEF3C7;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 10px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6B7280;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid #E5E7EB;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<h1 class="main-header">🚀 Projectile Dynamics Lab</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-header"><b>Department of Applied Sciences - Tarang Fest</b><br><i>A Computational Physics Simulation Platform</i></div>', unsafe_allow_html=True)

# ========== SIDEBAR ==========``
st.sidebar.markdown('<div class="sidebar-header"><h3>🌌 Simulation Control Panel</h3></div>', unsafe_allow_html=True)

# 1. LAUNCH PARAMETERS
st.sidebar.markdown("### 🎯 Launch Parameters")
col1, col2 = st.sidebar.columns(2)
with col1:
    velocity = st.slider("Velocity (m/s)", 10, 100, 30, 1, 
                        help="Initial launch velocity of the projectile")
with col2:
    angle = st.slider("Angle (°)", 15, 75, 45, 1,
                     help="Launch angle relative to horizontal")

# 2. ENVIRONMENT
st.sidebar.markdown("### 🌍 Environment")
gravity_mode = st.sidebar.selectbox(
    "Gravity Setting",
    ["Earth (9.81 m/s²)", "Moon (1.62 m/s²)", "Mars (3.71 m/s²)", "Jupiter (24.79 m/s²)"],
    index=0,
    help="Select planetary gravity environment"
)

gravity_map = {
    "Earth (9.81 m/s²)": 9.81,
    "Moon (1.62 m/s²)": 1.62,
    "Mars (3.71 m/s²)": 3.71,
    "Jupiter (24.79 m/s²)": 24.79
}
g = gravity_map[gravity_mode]

# Planet Image
st.sidebar.markdown("### 🪐 Selected Planet")
planet_name = gravity_mode.split(" ")[0]
planet_images = {
    "Earth": "earth.jpg",
    "Moon": "moon.jpg",
    "Mars": "mars.jpg",
    "Jupiter": "jupiter.jpg"
}

if planet_name in planet_images:
    image_path = f"assets/{planet_images[planet_name]}"
    if os.path.exists(image_path):
        try:
            planet_img = Image.open(image_path)
            planet_img.thumbnail((250, 150))
            st.sidebar.image(planet_img, caption=planet_name)
        except:
            st.sidebar.info(f"🌍 {planet_name}")
    else:
        st.sidebar.info(f"🌍 {planet_name}")

# 3. PROJECTILE PROPERTIES
st.sidebar.markdown("### ⚙️ Projectile Properties")
mass = st.sidebar.number_input("Mass (kg)", 0.01, 10.0, 0.1, 0.01,
                              help="Mass of the projectile")
radius = st.sidebar.number_input("Radius (m)", 0.01, 0.5, 0.05, 0.01,
                                help="Radius of spherical projectile")

# 4. SIMULATION OPTIONS
st.sidebar.markdown("### ⚡ Simulation Options")
show_ideal = st.sidebar.checkbox("Show Ideal Trajectory", True,
                                help="Display theoretical trajectory without drag")
enable_drag = st.sidebar.checkbox("Enable Air Resistance", True,
                                 help="Include atmospheric drag in simulation")

# Air density info
if planet_name in ["Moon", "Mars"]:
    st.sidebar.markdown('<div class="warning-box">⚠️ No significant atmosphere - drag has minimal effect</div>', unsafe_allow_html=True)

# Team Info
st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 Team Information")
st.sidebar.info("""
**Team Members:**
- **Team Lead**: Physics Modeling
- **Developer**: UI/Implementation
- **Researcher**: Data Analysis
- **Designer**: UX/Visualization
- **Tester**: Quality Assurance
""")

# ========== MAIN CONTENT ==========
# Initialize simulator
sim = ProjectileSimulator()

# Set environment
if 'earth' in planet_name.lower():
    sim.set_environment('earth')
elif 'moon' in planet_name.lower():
    sim.set_environment('moon')
elif 'mars' in planet_name.lower():
    sim.set_environment('mars')
else:
    sim.set_environment('earth')

# Calculate trajectories
try:
    # Ideal trajectory (no drag)
    x_ideal, y_ideal = sim.without_air_resistance(velocity, angle, g)
    
    # Realistic trajectory (with drag)
    if enable_drag:
        t_real, x_real, y_real = sim.with_air_resistance(velocity, angle, mass, radius)
    else:
        # Without drag, use ideal but with same time sampling
        x_real, y_real = x_ideal, y_ideal
        t_real = np.linspace(0, 2*velocity*np.sin(np.radians(angle))/g, len(x_real))
    
    # ========== VISUALIZATION ==========
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Create Plotly figure
        fig = go.Figure()
        
        # Add ideal trajectory
        if show_ideal and len(x_ideal) > 0:
            fig.add_trace(go.Scatter(
                x=x_ideal, y=y_ideal,
                mode='lines',
                name='Ideal (No Drag)',
                line=dict(color='#3B82F6', dash='dash', width=2),
                hovertemplate='<b>Ideal Trajectory</b><br>Distance: %{x:.1f} m<br>Height: %{y:.1f} m<extra></extra>'
            ))
        
        # Add realistic trajectory
        if len(x_real) > 0:
            fig.add_trace(go.Scatter(
                x=x_real, y=y_real,
                mode='lines',
                name='Realistic (With Drag)' if enable_drag else 'Trajectory',
                line=dict(color='#EF4444', width=3),
                hovertemplate='<b>Realistic Trajectory</b><br>Distance: %{x:.1f} m<br>Height: %{y:.1f} m<extra></extra>'
            ))
        
        # Add launch point
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            name='Launch Point',
            marker=dict(size=12, color='#10B981', symbol='circle'),
            hovertemplate='<b>Launch Point</b><br>(0, 0)<extra></extra>'
        ))
        
        # Update layout with CORRECT properties
        fig.update_layout(
            title=dict(
                text=f"Projectile Trajectory on {planet_name}",
                font=dict(size=24, color='#1F2937'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="Horizontal Distance (m)",
                title_font=dict(size=14),  # CORRECTED: title_font instead of titlefont
                gridcolor='#E5E7EB',
                zerolinecolor='#E5E7EB'
            ),
            yaxis=dict(
                title="Vertical Height (m)",
                title_font=dict(size=14),  # CORRECTED: title_font instead of titlefont
                gridcolor='#E5E7EB',
                zerolinecolor='#E5E7EB'
            ),
            hovermode='x unified',
            height=550,
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.02,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#E5E7EB',
                borderwidth=1
            ),
            margin=dict(l=50, r=30, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ========== PERFORMANCE METRICS ==========
        st.markdown("### 📊 Performance Metrics")
        
        if len(x_ideal) > 0 and len(x_real) > 0:
            # Calculate metrics
            ideal_range = float(x_ideal[-1])
            real_range = float(x_real[-1])
            ideal_height = float(np.max(y_ideal))
            real_height = float(np.max(y_real))
            
            ideal_time = 2 * velocity * np.sin(np.radians(angle)) / g
            real_time = float(t_real[-1]) if len(t_real) > 0 else ideal_time
            
            # Range Metric
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Range</div>
                <div class="metric-value">{:.1f} m</div>
            """.format(real_range), unsafe_allow_html=True)
            
            if enable_drag and ideal_range > 0:
                range_reduction = ((ideal_range - real_range) / ideal_range) * 100
                st.markdown('<div class="metric-delta" style="color: #DC2626;">-{:.1f}% due to drag</div></div>'.format(range_reduction), unsafe_allow_html=True)
            else:
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Max Height Metric
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Maximum Height</div>
                <div class="metric-value">{:.1f} m</div>
            """.format(real_height), unsafe_allow_html=True)
            
            if enable_drag and ideal_height > 0:
                height_reduction = ((ideal_height - real_height) / ideal_height) * 100
                st.markdown('<div class="metric-delta" style="color: #DC2626;">-{:.1f}% due to drag</div></div>'.format(height_reduction), unsafe_allow_html=True)
            else:
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Time of Flight
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Time of Flight</div>
                <div class="metric-value">{:.2f} s</div>
            """.format(real_time), unsafe_allow_html=True)
            
            if enable_drag:
                time_reduction = ((ideal_time - real_time) / ideal_time) * 100
                st.markdown('<div class="metric-delta" style="color: #DC2626;">-{:.1f}% due to drag</div></div>'.format(time_reduction), unsafe_allow_html=True)
            else:
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Efficiency Metrics
            # Efficiency Metrics
            if enable_drag and ideal_range > 0:
                st.markdown("### 📉 Efficiency Analysis")
    
            # Calculate efficiencies
            range_efficiency = (real_range / ideal_range) * 100 if ideal_range > 0 else 0
            height_efficiency = (real_height / ideal_height) * 100 if ideal_height > 0 else 0
            
            # FIX: Ensure values are between 0 and 100
            range_efficiency = max(0, min(range_efficiency, 100))
            height_efficiency = max(0, min(height_efficiency, 100))
            
            # Progress bars - FIXED with proper 0-1 range
            st.markdown("**Range Efficiency:**")
            progress_range_value = float(range_efficiency / 100.0)  # Convert to 0.0-1.0
            st.progress(progress_range_value)
            st.caption(f"{range_efficiency:.1f}% of ideal range")
            
            st.markdown("**Height Efficiency:**")
            progress_height_value = float(height_efficiency / 100.0)  # Convert to 0.0-1.0
            st.progress(progress_height_value)
            st.caption(f"{height_efficiency:.1f}% of ideal height")
            
           
            
            # Optimal angle check
            if angle == 45:
                st.success("🎯 **Optimal Angle**: 45° for maximum range (without drag)")
            elif angle < 45:
                st.info("📐 **Angle Note**: Below optimal 45° for maximum range")
            else:
                st.info("📐 **Angle Note**: Above optimal 45° for maximum range")
    
    # ========== PHYSICS ANALYSIS SECTION ==========
    st.markdown("---")
    st.markdown("### 🔬 Physics Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Physics Principles", "🌍 Applications", "👥 Our Team", "🎯 Quick Guide"])
    
    with tab1:
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.markdown("""
            #### **Core Physics Equations**
            
            **Ideal Motion (No Air Resistance):**
            $$
            \\begin{aligned}
            x(t) &= v_0 \\cos\\theta \\cdot t \\\\
            y(t) &= v_0 \\sin\\theta \\cdot t - \\frac{1}{2}gt^2
            \\end{aligned}
            $$
            
            **With Air Resistance (Drag Force):**
            $$
            F_d = \\frac{1}{2} \\rho C_d A v^2
            $$
            
            **Numerical Solution:**
            Using 4th Order Runge-Kutta method:
            $$
            \\frac{d^2\\vec{r}}{dt^2} = \\vec{g} - \\frac{\\vec{F_d}}{m}
            $$
            """)
        
        with col_b:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("""
            #### **Current Simulation Parameters**
            
            **Projectile:**
            - Mass: {:.2f} kg
            - Radius: {:.2f} m
            - Cross-sectional Area: {:.4f} m²
            
            **Environment:**
            - Planet: {}
            - Gravity: {:.2f} m/s²
            - Air Density: {:.3f} kg/m³
            """.format(mass, radius, np.pi * radius**2, planet_name, g, sim.rho))
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        #### **Real-world Engineering Applications**
        
        | Application | Relevance |
        |-------------|-----------|
        | **🚀 Space Missions** | Re-entry vehicle trajectory planning |
        | **🎯 Military Ballistics** | Artillery shell and missile guidance |
        | **⛳ Sports Science** | Golf ball and javelin aerodynamics |
        | **🔥 Firefighting** | Optimal water jet trajectories |
        | **🏗️ Civil Engineering** | Fountain and waterfall design |
        | **🌍 Environmental Science** | Air pollutant dispersion modeling |
        
        #### **BTech Career Applications**
        - **Aerospace Engineering**: Rocket trajectory optimization
        - **Mechanical Engineering**: Projectile system design
        - **Data Science**: Physics-informed machine learning models
        - **Research & Development**: Computational physics simulations
        """)
    
    with tab3:
        st.markdown("""
        #### **👥 Meet Our Team**
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center; margin: 20px 0;">
        <h3 style="color: white; margin: 0;">Team Tarang</h3>
        <p style="color: white; opacity: 0.9;">Department of Applied Sciences</p>
        <p style="color: white; font-size: 1.1rem; margin-top: 10px;">Computational Physics & Engineering Simulation</p>
        </div>
        
        **Team Roles & Contributions:**
        
        | Member | Role | Key Contributions |
        |--------|------|-------------------|
        | **Team Lead** | Project Management | Physics modeling, ODE integration, Team coordination |
        | **Lead Developer** | Backend Development | Simulation engine, Numerical methods, Algorithm design |
        | **UI/UX Designer** | Frontend Development | Streamlit interface, Data visualization, User experience |
        | **Research Analyst** | Data Science | Model validation, Parameter analysis, Documentation |
        | **Quality Analyst** | Testing | Performance testing, Bug fixing, Presentation prep |
        
        **Technology Stack:**
        - **Python**: Core programming language
        - **Streamlit**: Web application framework
        - **Plotly**: Interactive data visualization
        - **NumPy/SciPy**: Scientific computing libraries
        - **NASA Data**: Planetary images and parameters
        """)
    
    with tab4:
        st.markdown("""
        #### **🎯 Quick User Guide**
        
        **1. Set Launch Parameters:**
           - Adjust velocity (10-100 m/s)
           - Set launch angle (15-75°)
           - Optimal angle for max range: 45° (without drag)
        
        **2. Choose Environment:**
           - Select planet for different gravity
           - Earth: 9.81 m/s² with atmosphere
           - Moon: 1.62 m/s², no atmosphere
           - Mars: 3.71 m/s², thin atmosphere
           - Jupiter: 24.79 m/s², dense atmosphere
        
        **3. Configure Projectile:**
           - Mass affects inertia
           - Radius affects drag (larger = more drag)
        
        **4. Simulation Options:**
           - Toggle air resistance on/off
           - Compare with ideal trajectory
           - Observe efficiency metrics
        
        **💡 Pro Tips:**
        - Try **Moon** gravity to see exaggerated trajectories
        - Compare **with/without drag** to understand air resistance effects
        - Use **45° angle** for maximum theoretical range
        - Increase **radius** to see significant drag effects
        """)
    
    # ========== FOOTER ==========
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Developed for:**  
        🎪 Tarang Fest 2026  
        Department of Applied Sciences
        """)
    
    with col2:
        st.markdown("""
        **Technology:**  
        Python • Streamlit • Plotly  
        NumPy • SciPy • NASA Data
        """)
    
    with col3:
        st.markdown("""
        **Image Credits:**  
        NASA Earth Observatory  
        NASA Lunar Reconnaissance Orbiter
        """)
    
    # ========== SIDEBAR CONTROLS ==========
    st.sidebar.markdown("---")
    
    # Export Data
    if st.sidebar.button("💾 Export Simulation Data", use_container_width=True):
        import pandas as pd
        if len(x_real) > 0:
            df = pd.DataFrame({
                'Time': t_real,
                'X_Position': x_real,
                'Y_Position': y_real,
                'Velocity': velocity,
                'Angle': angle,
                'Planet': planet_name,
                'Gravity': g,
                'Mass': mass,
                'Radius': radius
            })
            csv = df.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"projectile_{planet_name}_{velocity}mps_{angle}deg.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.sidebar.warning("Run simulation first")
    
    # Reset Button
    if st.sidebar.button("🔄 Reset to Defaults", use_container_width=True):
        st.experimental_rerun()

except Exception as e:
    st.error(f"❌ Simulation Error: {str(e)}")
    st.info("Please adjust parameters and try again.")

# ========== LOADING INDICATOR ==========
if 'x_ideal' in locals() and 'x_real' in locals():
    if len(x_ideal) > 0 and len(x_real) > 0:
        #st.balloons()
        st.success("✅ Simulation complete! Explore different parameters to see how they affect the trajectory.")