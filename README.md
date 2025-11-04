# Traffic Visualiser 🚦

A sophisticated real-time traffic signal simulation system built with Python and Pygame. This project provides a realistic visualization of a four-way traffic intersection with intelligent signal control, multiple vehicle types, and dynamic traffic flow management.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Screenshots](#screenshots)
- [Applications](#applications)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Traffic Visualiser simulates a realistic four-way traffic intersection with automated signal control. The system manages vehicle spawning, movement, collision detection, and traffic light timing to create an authentic urban traffic scenario. This project is ideal for educational purposes, traffic engineering demonstrations, and algorithm testing.

## ✨ Features

### Core Functionality
- **Multi-directional Traffic Flow**: Four-way intersection with right, down, left, and up traffic directions
- **Intelligent Signal Control**: Automated traffic light system with configurable timing
- **Multiple Vehicle Types**: Support for cars, buses, trucks, bikes, and rickshaws
- **Realistic Vehicle Behavior**: Speed variation, stopping at red lights, and smooth acceleration
- **Dynamic Vehicle Spawning**: Random vehicle generation with type distribution
- **Collision Detection**: Vehicles maintain safe distances and queue properly
- **Real-time Visualization**: Smooth Pygame-based graphics with 60 FPS rendering

### Vehicle Management
- **5 Vehicle Types**: Each with unique dimensions and characteristics
  - Cars
  - Buses
  - Trucks
  - Bikes
  - Rickshaws
- **Random Spawning**: Vehicles appear at configurable intervals
- **Lane Discipline**: Vehicles stay in designated lanes
- **Turning Logic**: Support for right, left, and straight movements

### Signal System
- **Automated Timing**: Configurable green, yellow, and red signal durations
- **Sequential Control**: Signals change in a defined order (right → down → left → up)
- **Yellow Light Phase**: Transition period between green and red
- **Visual Indicators**: Clear signal state display for each direction

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/rahulkumar7189/traffic_visualiser.git
   cd traffic_visualiser
   ```

2. **Install required dependencies**
   ```bash
   pip install pygame
   ```

3. **Verify installation**
   ```bash
   python --version
   pip show pygame
   ```

## 💻 Usage

### Basic Usage

Run the simulation with default settings:

```bash
python traffic_visualiser.py
```

The simulation window will open, displaying:
- A four-way intersection
- Traffic lights in each direction
- Vehicles spawning and moving according to signal states
- Real-time traffic flow visualization

### Controls

- **Close Window**: Click the X button or press Alt+F4 to exit
- The simulation runs continuously until manually stopped

### Understanding the Display

- **Green Light**: Vehicles in that direction can proceed
- **Yellow Light**: Transition phase, vehicles should prepare to stop
- **Red Light**: Vehicles must stop and wait
- **Vehicle Colors**: Different colors represent different vehicle types
- **Coordinates Display**: Shows signal and vehicle positions (for debugging)

## 🔧 How It Works

### Architecture

The system consists of three main classes:

1. **TrafficSignal**: Manages traffic light states and timing
   - Controls red, yellow, and green signal durations
   - Handles automatic signal transitions
   - Maintains signal state for each direction

2. **Vehicle**: Represents individual vehicles in the simulation
   - Stores vehicle properties (type, position, speed, direction)
   - Handles movement logic and stopping behavior
   - Manages vehicle rendering

3. **Main Simulation Loop**: Coordinates the entire system
   - Spawns vehicles at random intervals
   - Updates vehicle positions
   - Manages signal transitions
   - Renders all elements to the screen

### Traffic Flow Logic

1. Vehicles spawn at entry points for each direction
2. They move at their designated speed until:
   - A red or yellow light is encountered
   - Another vehicle is too close ahead
3. Vehicles stop and queue when necessary
4. When the light turns green, vehicles accelerate and proceed
5. Vehicles exit the simulation after crossing the intersection

### Signal Timing Algorithm

```
Default Timing:
- Green Signal: 5 seconds
- Yellow Signal: 5 seconds  
- Red Signal: Variable (depends on other signals)

Sequence: Right → Down → Left → Up → Repeat
```

## ⚙️ Customization

You can customize various parameters by modifying the code:

### Adjust Signal Timing

```python
# Find this section in the code
defaultGreen = {0:10, 1:10, 2:10, 3:10}  # Green light duration
defaultYellow = 5  # Yellow light duration
defaultRed = 150  # Initial red duration
```

### Modify Vehicle Spawn Rate

```python
# Adjust the spawn interval (in milliseconds)
if ts >= timeGap:
    ts = 0
    # Modify the vehicle generation logic here
```

### Change Vehicle Speed

```python
# Modify speeds dictionary
speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5, 'rickshaw':2.0}
```

### Adjust Window Size

```python
screenWidth = 1400
screenHeight = 800
```

### Configure Vehicle Distribution

```python
# Adjust the vehicle type distribution in the vehicle generation logic
typeOfVehicle = random.randint(0,4)  # 0:car, 1:bus, 2:truck, 3:bike, 4:rickshaw
```

## 📸 Screenshots

_Add screenshots of your simulation here to showcase:_
- Main intersection view
- Different traffic scenarios
- Various vehicle types in action
- Signal state transitions

## 🎓 Applications

This traffic simulation can be used for:

### Educational
- **Traffic Engineering**: Demonstrate signal timing optimization
- **Computer Science**: Illustrate object-oriented programming concepts
- **Game Development**: Learn Pygame basics and animation techniques
- **Algorithm Design**: Test traffic flow algorithms

### Research & Development
- **Signal Timing Optimization**: Experiment with different timing strategies
- **Traffic Flow Analysis**: Study vehicle queue formation and dissipation
- **Congestion Studies**: Model intersection capacity and bottlenecks
- **Intelligent Transportation Systems**: Test adaptive signal control algorithms

### Professional
- **Urban Planning**: Visualize proposed intersection designs
- **Smart City Projects**: Prototype traffic management systems
- **Simulation Training**: Create scenarios for traffic controller training

## 🔬 Technical Details

### Technologies Used
- **Python**: Core programming language
- **Pygame**: Graphics rendering and game loop management
- **Random Module**: Vehicle generation and type selection
- **Time Module**: Signal timing and frame rate control

### Key Parameters
- **Simulation FPS**: 60 frames per second
- **Default Screen Size**: 1400x800 pixels
- **Vehicle Types**: 5 distinct types with unique properties
- **Traffic Directions**: 4 (right, down, left, up)
- **Signal States**: 3 per direction (red, yellow, green)

### Performance Considerations
- Efficient collision detection using position-based checks
- Optimized rendering with Pygame's blit operations
- Proper memory management for spawned and despawned vehicles
- Frame-rate independent timing for consistent behavior

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions
- Add pedestrian crossing simulation
- Implement emergency vehicle priority
- Create adaptive signal timing based on traffic density
- Add sound effects for vehicle movement and signals
- Implement vehicle turning animations
- Add traffic violation detection
- Create statistics dashboard (throughput, wait times, etc.)
- Support for roundabouts or complex intersections

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rahul Kumar**
- GitHub: [@rahulkumar7189](https://github.com/rahulkumar7189)

## 🙏 Acknowledgments

- Pygame community for excellent documentation and examples
- Traffic engineering principles for realistic signal timing
- Open source community for inspiration and support

## 📞 Support

If you have any questions, issues, or suggestions:
- Open an issue on GitHub
- Star the repository if you find it useful
- Share with others who might benefit

---

**Note**: This is a simulation for educational and demonstration purposes. Real-world traffic systems require extensive testing, safety validation, and regulatory compliance.
