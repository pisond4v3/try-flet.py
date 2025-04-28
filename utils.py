from datetime import datetime, timedelta

# Shared component data
COMPONENT_DATA = {
    "Engine Oil & Oil Filter": {
        "images": {
            "Synthetic Oil": "assets/componentskind_icon/fully-synthetic_oil.png",
            "Conventional Oil": "assets/componentskind_icon/conventional-oil.png",
            "Semi-Synthetic Oil": "assets/componentskind_icon/semi-synthetic_oil.png"
        },
        "definitions": {
            "Synthetic Oil": "Synthetic oil is a lubricant made from artificially created chemical compounds, often derived from petroleum but with molecules engineered for specific performance characteristics, offering potential advantages over conventional oil in terms of stability and performance.",
            "Conventional Oil": "Conventional oil is a natural lubricant derived from crude oil, offering basic engine protection and performance. It's the most commonly used oil type and is generally more affordable than synthetic options, though it may require more frequent changes.",
            "Semi-Synthetic Oil": "Semi-synthetic oil is a blend of conventional and synthetic oils, designed to offer a balance of performance and cost. It provides better engine protection and performance than conventional oil, while being more affordable than fully synthetic oil."
        },
        "options": ["Synthetic Oil", "Conventional Oil", "Semi-Synthetic Oil"]
    },
    "Air Filter": {
        "images": {
            "default": "assets/componentskind_icon/airfilter.png"
        },
        "definitions": {
            "default": "An air filter is a crucial component of an engine's intake system, designed to prevent dirt, debris, and other contaminants from entering the engine. It ensures that only clean air reaches the engine, helping to maintain optimal performance, improve fuel efficiency, and extend engine life. Regular maintenance and replacement of the air filter are essential for keeping the engine running smoothly."
        },
        "options": []
    },
    "Tires": {
        "images": {
            "All-Season Tires": "assets/componentskind_icon/allseason-tires.png",
            "Performance Tires": "assets/componentskind_icon/performance-tires.png",
            "Off-Road Tires": "assets/componentskind_icon/offroad-tires.png",
            "Run-Flat Tires": "assets/componentskind_icon/runflat-tires.png"
        },
        "definitions": {
            "All-Season Tires": "Designed for year-round use, offering a balance of performance in dry, wet, and light winter conditions.",
            "Performance Tires": "Built for enhanced handling and grip, especially at higher speeds—ideal for sporty driving.",
            "Off-Road Tires": "Engineered with rugged tread patterns for traction on dirt, mud, rocks, and uneven terrain.",
            "Run-Flat Tires": "Allow you to keep driving temporarily after a puncture, giving you time to reach a repair shop safely.",
        },
        "options": ["All-Season Tires", "Performance Tires", "Off-Road Tires", "Run-Flat Tires"]
    },
    "Brake Fluid and Pads": {
        "images": {
            "Organic (Non-Metallic)": "assets/componentskind_icon/organic-brakepads.png",
            "Semi-Metallic": "assets/componentskind_icon/semi-Metallic-brakepads.png",
            "Ceramic": "assets/componentskind_icon/ceramic-brakepads.png"
        },
        "definitions": {
            "Organic (Non-Metallic)": "Organic brake pads are made from natural materials like rubber, resin, and fibers, offering quiet and smooth braking. They are ideal for light driving but wear faster and create more dust than other types.",
            "Semi-Metallic": "Semi-metallic brake pads combine metal particles with synthetic materials for strong braking performance and durability. They're suitable for high-performance and daily use, though they can be noisier and tougher on rotors.",
            "Ceramic": "Ceramic brake pads are made from dense ceramic material mixed with fine metal fibers, providing clean, quiet, and consistent braking. They last longer and produce less dust, but are usually more expensive than other pad types."
        },
        "options": ["Organic (Non-Metallic)", "Semi-Metallic", "Ceramic"]
    },
    "Battery": {
        "images": {
            "Lead-Acid Battery": "assets/componentskind_icon/leadacid-battery.png",
            "AGM (Absorbent Glass Mat) Battery": "assets/componentskind_icon/agm-battery.png",
        },
        "definitions": {
            "Lead-Acid Battery": "This is the most common type of battery found in traditional gasoline and diesel vehicles. It's affordable and reliable for starting engines and powering basic electrical systems, but it's relatively heavy and may require regular maintenance like checking fluid levels.",
            "AGM (Absorbent Glass Mat) Battery": "A more advanced version of the lead-acid battery, AGM uses a special glass mat separator to absorb the electrolyte, making it spill-proof and maintenance-free. It offers better performance, faster charging, and longer lifespan, especially in vehicles with high electrical demands or start-stop systems.",
        },
        "options": ["Lead-Acid Battery", "AGM (Absorbent Glass Mat) Battery"]
    },
    "Transmission Fluid": {
        "images": {
            "Manual Transmission": "assets/componentskind_icon/manual-transmissionfluid.png",
            "Automatic Transmission (AT)": "assets/componentskind_icon/automatic-transmissionfluid.png",
            "Continuously Variable Transmission (CVT)": "assets/componentskind_icon/cvt-transmissionfluid.png",
            "Dual-Clutch Transmission (DCT)": "assets/componentskind_icon/dct-transmissionfluid.png"
        },
        "definitions": {
            "Manual Transmission": "Fluid for manual gear shifting: Manual transmission uses a driver-operated clutch and gear stick to manually shift gears, offering full control and typically better fuel efficiency. It's known for mechanical simplicity and lower maintenance costs but requires more driving skill.",
            "Automatic Transmission (AT)": "Fluid for automatic gear shifting: Automatic transmission shifts gears automatically based on speed and load, providing a smoother and more convenient driving experience. It's user-friendly and ideal for city driving, though it can be less fuel-efficient than manuals.",
            "Continuously Variable Transmission (CVT)": "Special fluid for CVT systems.:CVT uses a system of pulleys and a belt to provide seamless gear transitions without fixed gear steps. It offers smooth acceleration and optimal fuel efficiency, but may lack the 'feel' of traditional gear shifts.",
            "Dual-Clutch Transmission (DCT)": "Fluid for dual-clutch systems.: DCT uses two separate clutches for odd and even gears, enabling lightning-fast gear changes without interrupting power flow. It delivers sporty performance and efficiency, though it can be more complex and expensive to maintain."
        },
        "options": ["Manual Transmission", "Automatic Transmission (AT)", "Continuously Variable Transmission (CVT)", "Dual-Clutch Transmission (DCT)"]
    },
    "Coolant (Radiator Fluid)": {
        "images": {
            "Ethylene Glycol-Based (Green/Traditional)": "assets/componentskind_icon/ethylene-Glycol-Based.png",
            "Extended Life Coolant (OAT/HOAT – Orange, Pink, Red, etc.)": "assets/componentskind_icon/extended-Life-Coolant.png"
        },
        "definitions": {
            "Ethylene Glycol-Based (Green/Traditional)": "This type of coolant uses inorganic additives to prevent corrosion and overheating in the engine. It is typically used in older vehicles and needs to be replaced every 2 to 3 years.",
            "Extended Life Coolant (OAT/HOAT – Orange, Pink, Red, etc.)": "Extended life coolant uses organic or hybrid additives for improved protection and longer service intervals. It's suitable for modern engines and can last up to 5 years or more, with colors varying by formulation."
        },
        "options": ["Ethylene Glycol-Based (Green/Traditional)", "Extended Life Coolant (OAT/HOAT – Orange, Pink, Red, etc.)"]
    },
    "Fuel Filter": {
        "images": {
            "Regular Gasoline": "assets/componentskind_icon/regulargas-fuelfilter.png",
            "Premium Gasoline": "assets/componentskind_icon/premiumgas-fuelfilter.png",
            "Diesel": "assets/componentskind_icon/diesel-fuelfilter.png",
            "Ethanol-Blended Fuel (E85)": "assets/componentskind_icon/ethanol-Blended-fuelfilter.png"
        },
        "definitions": {
            "Regular Gasoline": "Filter for standard gasoline engines.:Regular gasoline is the most commonly used fuel, typically rated at 87 octane. It's suitable for most standard engines and offers a good balance of performance and affordability.",
            "Premium Gasoline": "Filter for high-performance gasoline engines.:Premium gasoline has a higher octane rating, usually 91 or higher, designed for high-performance or turbocharged engines. It helps prevent knocking and can improve engine efficiency in vehicles that require it.",
            "Diesel": "Filter designed for diesel fuel systems.:Diesel fuel is used in compression-ignition engines and provides higher torque and fuel efficiency compared to gasoline. It's commonly used in trucks, SUVs, and commercial vehicles.",
            "Ethanol-Blended Fuel (E85)": "Filter for ethanol-blended fuels.:E85 is a blend of 85% ethanol and 15% gasoline, mainly used in flex-fuel vehicles. It burns cleaner than regular gasoline but typically delivers lower fuel economy."
        },
        "options": ["Regular Gasoline", "Premium Gasoline", "Diesel", "Ethanol-Blended Fuel (E85)"]
    }
}

def calculate_status_and_schedule(vehicle_data, component_name, last_maintenance_date_str, component_type):
    """
    Calculate the maintenance status and schedule for a component.

    Args:
        vehicle_data (dict): Data about the vehicle, where km_usage is the kilometers since last maintenance.
        component_name (str): Name of the component (e.g., "Engine Oil & Oil Filter").
        last_maintenance_date_str (str): Last maintenance date in "MM/DD/YYYY" format.
        component_type (str): Type of the component (e.g., "Synthetic Oil").

    Returns:
        tuple: (status, estimated_schedule, km_remaining, reasons)
            - status (str): "Excellent", "Good", "Fair", or "Critical".
            - estimated_schedule (str): Next maintenance date in "MM/DD/YYYY" format.
            - km_remaining (int): Kilometers remaining until next maintenance.
            - reasons (list): List of reasons for the prediction.
    """
    try:
        last_maintenance_date = datetime.strptime(last_maintenance_date_str, "%m/%d/%Y")

        # Get maintenance intervals based on component type
        component_key = component_type or "default"
        intervals = COMPONENT_DATA.get(component_name, {}).get("maintenance_intervals", {}).get(component_key,
                                                                                               {"km": 5000,
                                                                                                "months": 6})
        km_interval = intervals["km"]
        months_interval = intervals["months"]

        # Calculate next maintenance date based on time
        next_maintenance_date = last_maintenance_date + timedelta(
            days=months_interval * 30)  # Approximate months to days

        # Calculate kilometers since last maintenance
        km_since_last = vehicle_data.get("km_usage", 0)  # km_usage should be the kilometers since last maintenance
        km_remaining = max(0, km_interval - km_since_last)

        # Determine status based on km_remaining and time remaining
        months_remaining = (next_maintenance_date - datetime.now()).days / 30.0
        km_percentage = (km_remaining / km_interval) * 100
        time_percentage = (months_remaining / months_interval) * 100
        overall_percentage = min(km_percentage, time_percentage)

        if overall_percentage > 75:
            status = "Excellent"
        elif overall_percentage > 50:
            status = "Good"
        elif overall_percentage > 25:
            status = "Fair"
        else:
            status = "Critical"

        estimated_schedule = next_maintenance_date.strftime("%m/%d/%Y")
        reasons = [
            f"Based on last maintenance date: {last_maintenance_date_str}",
            f"KM since last maintenance: {km_since_last:,} km",
            f"KM interval for {component_type}: {km_interval:,} km",
            f"Time interval for {component_type}: {months_interval} months"
        ]
        return status, estimated_schedule, km_remaining, reasons

    except Exception as e:
        return "N/A", "N/A", 0, [f"Error calculating schedule: {str(e)}"]