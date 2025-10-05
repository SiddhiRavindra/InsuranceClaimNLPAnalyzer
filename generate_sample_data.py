# import pandas as pd

# # Sample insurance claims data
# claims_data = {
#     'claim_id': ['CLM001', 'CLM002', 'CLM003', 'CLM004', 'CLM005', 'CLM006'],
#     'description': [
#         "On March 15, 2024, my 2019 Honda Accord was rear-ended at the intersection of Main St and Oak Ave in Boston. The other driver ran a red light. Significant damage to rear bumper and trunk. Police report filed.",
        
#         "Minor fender bender in parking lot on 01/20/2024. Small scratch on driver side door of my Toyota Camry. No injuries. Other party admitted fault.",
        
#         "URGENT: My house at 123 Elm Street, Cambridge was severely damaged by fire on February 10th. Entire kitchen destroyed, smoke damage throughout second floor. Fire department report available. Estimated damage over $150,000.",
        
#         "Windshield crack appeared suddenly while driving on highway yesterday. No accident, possibly hit by small rock. 2021 Tesla Model 3. Needs replacement.",
        
#         "Claimed stolen vehicle from 456 Park Ave, Boston on 03/01/2024 but later found it in different parking lot where I forgot I parked it. False alarm, please disregard.",
        
#         "Total loss - my 2018 Ford F-150 was completely submerged during flooding on River Road. Water damage to engine and interior. Vehicle is not drivable. Need immediate assistance."
#     ],
#     'actual_severity': ['High', 'Low', 'High', 'Low', 'Low', 'High']
# }

# df = pd.DataFrame(claims_data)
# df.to_csv('sample_claims.csv', index=False)
# print("Sample claims data generated successfully!")
# print(f"Created {len(df)} sample claims in 'sample_claims.csv'")
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_insurance_claims(num_claims=500):
    """
    Generate diverse insurance claims dataset
    """
    
    # Data pools for variety
    cities = [
        "Boston", "Cambridge", "Somerville", "Brookline", "Newton",
        "Quincy", "Lynn", "Malden", "Medford", "Waltham",
        "Worcester", "Springfield", "Lowell", "Providence", "Hartford"
    ]
    
    streets = [
        "Main St", "Oak Ave", "Elm Street", "Washington Blvd", "Park Ave",
        "Broadway", "Maple Drive", "Cedar Lane", "Pine Road", "River Road",
        "Lake Street", "Hill Ave", "Forest Drive", "Church St", "School Road",
        "Highland Ave", "Union Street", "Pleasant St", "Spring St", "Summer St"
    ]
    
    vehicles = [
        "2019 Honda Accord", "2020 Toyota Camry", "2021 Tesla Model 3",
        "2018 Ford F-150", "2022 BMW X5", "2020 Chevrolet Silverado",
        "2019 Nissan Altima", "2021 Mazda CX-5", "2020 Subaru Outback",
        "2018 Jeep Wrangler", "2022 Mercedes-Benz C-Class", "2019 Hyundai Elantra",
        "2020 Kia Sorento", "2021 Volkswagen Jetta", "2019 Audi A4",
        "2020 Lexus RX", "2021 Volvo XC90", "2018 Dodge Ram",
        "2022 Acura MDX", "2020 GMC Sierra", "2019 Infiniti Q50"
    ]
    
    parts = [
        "driver side door", "rear bumper", "front bumper", "hood",
        "passenger side", "trunk", "fender", "quarter panel",
        "headlight", "tail light", "side mirror", "windshield"
    ]
    
    # Claim templates by severity
    templates = {
        'Low': [
            "Minor parking lot incident on {date}. Small scratch on {part} of my {vehicle}. No injuries. Other party left contact information.",
            "Windshield chip from road debris on {date} while driving on {street}. {vehicle}. Small chip needs repair before it spreads.",
            "Shopping cart dent on {part} at {city} shopping center on {date}. {vehicle}. Superficial damage only.",
            "Minor scrape on {part} while parking on {date} at {location}. {vehicle}. Paint transfer visible.",
            "Small dent from hail storm on {date}. {vehicle} parked at {location}. {part} affected.",
            "Broken {part} discovered on {date} at {location}. Likely vandalism while parked. {vehicle}.",
            "Minor bumper contact in parking garage on {date}. {vehicle}. Both parties exchanged information.",
            "Tire damage from pothole on {street} on {date}. {vehicle}. Tire needs replacement.",
            "Small scratch along {part} noticed on {date}. Unknown cause. {vehicle} parked at {location}.",
            "Bird damage to paint on hood on {date}. {vehicle}. Etching visible, needs touch-up."
        ],
        
        'Medium': [
            "Rear-ended at intersection of {street1} and {street2} in {city} on {date}. My {vehicle} sustained moderate damage to {part}. Police report filed.",
            "Side-swiped on highway near {city} on {date}. {vehicle} has damage to {part} and {part2}. Other driver cited for unsafe lane change.",
            "Backed into pole in parking lot on {date} at {location}. {vehicle} has dent in {part}. My fault, estimated repair cost $3,500.",
            "Hit by opening car door on {date} at {location}. Damage to {part} of my {vehicle}. Other party admitted fault.",
            "Vehicle struck by falling branch during storm on {date}. {vehicle} has damage to {part} and windshield. Tree maintenance company notified.",
            "Collision with deer on {street} near {city} on {date}. {vehicle} has front-end damage including {part} and {part2}. Police report available.",
            "Hit and run while parked on {date} at {location}. {vehicle} has significant damage to {part}. Witnesses provided partial plate number.",
            "Fender bender on {date} at {street1} in {city}. {vehicle} damage to {part}. Both drivers remained at scene.",
            "Vehicle damaged by shopping cart blown by wind on {date}. {vehicle} has dents on {part}. Security footage available.",
            "Minor collision at stoplight on {date}. {vehicle} bumped from behind. Damage to {part}."
        ],
        
        'High': [
            "URGENT: Major collision on {date} at {street1} and {street2} in {city}. My {vehicle} was hit by driver who ran red light. Extensive damage to {part}, {part2}, and {part3}. Airbags deployed. Multiple injuries. Police and ambulance responded. Need immediate assistance.",
            "Total loss - {vehicle} completely submerged during flooding on {street} near {city} on {date}. Water reached dashboard level. Engine and interior destroyed. Vehicle not drivable. Towing required.",
            "Severe accident on highway near {city} on {date}. {vehicle} struck by semi-truck. Major damage to entire {part} side. Vehicle towed from scene. Hospital treatment required. Police report number {report_num}.",
            "URGENT: House fire at {address} {street}, {city} on {date}. Kitchen completely destroyed. Smoke and fire damage throughout first floor. Estimated damage ${amount}. Fire department report available. Family displaced.",
            "Devastating hail storm on {date} damaged {vehicle} and property. Multiple dents across hood, roof, and trunk. Windows cracked. Vehicle requires extensive repairs. Storm damage assessment needed.",
            "Head-on collision on {street} near {city} on {date}. {vehicle} sustained catastrophic front-end damage. Engine likely destroyed. Airbags deployed. Emergency services on scene. Vehicle total loss.",
            "My {vehicle} was struck by drunk driver on {date} at {location}. Extensive damage to {part}, {part2}, and frame. Police arrested other driver at scene. Vehicle likely totaled. Injuries sustained.",
            "Tree fell on {vehicle} during severe storm on {date} at {address} {street}, {city}. Roof crushed, all windows broken. Vehicle not drivable. Major structural damage. Storm damage claim.",
            "Multi-vehicle pileup on {date} on highway near {city}. {vehicle} sandwiched between two vehicles. Damage to front and rear including {part}, {part2}, {part3}. Major traffic incident with police investigation ongoing.",
            "URGENT: {vehicle} stolen from {location} on {date}. Vehicle found abandoned three days later with severe damage. {part} and {part2} destroyed. Interior vandalized. Police report filed. Recovery investigation ongoing."
        ]
    }
    
    # Generate claims
    claims_data = []
    
    for i in range(num_claims):
        claim_id = f"CLM{i+1:05d}"
        
        # Determine severity (60% Low, 30% Medium, 10% High)
        rand = random.random()
        if rand < 0.60:
            severity = 'Low'
        elif rand < 0.90:
            severity = 'Medium'
        else:
            severity = 'High'
        
        # Select random template
        template = random.choice(templates[severity])
        
        # Generate random date (last 12 months)
        days_ago = random.randint(1, 365)
        claim_date = datetime.now() - timedelta(days=days_ago)
        
        # Format variations
        date_formats = [
            claim_date.strftime("%B %d, %Y"),
            claim_date.strftime("%m/%d/%Y"),
            f"{days_ago} days ago"
        ]
        
        # Fill template
        description = template.format(
            date=random.choice(date_formats),
            vehicle=random.choice(vehicles),
            city=random.choice(cities),
            location=f"{random.choice(cities)} {random.choice(['Mall', 'Plaza', 'Shopping Center', 'Parking Garage'])}",
            street=random.choice(streets),
            street1=random.choice(streets),
            street2=random.choice(streets),
            part=random.choice(parts),
            part2=random.choice([p for p in parts]),
            part3=random.choice([p for p in parts]),
            address=random.randint(100, 9999),
            amount=random.choice(["50,000", "75,000", "100,000", "150,000", "200,000"]),
            report_num=f"RPT{random.randint(100000, 999999)}"
        )
        
        claims_data.append({
            'claim_id': claim_id,
            'description': description,
            'actual_severity': severity,
            'filing_date': claim_date.strftime("%Y-%m-%d")
        })
    
    return pd.DataFrame(claims_data)


# Generate datasets
if __name__ == "__main__":
    print("Generating insurance claims datasets...\n")
    
    # Generate sample_claims.csv (for app demo)
    print("Generating sample_claims.csv (50 claims for demo)...")
    df_demo = generate_insurance_claims(50)
    df_demo.to_csv('sample_claims.csv', index=False)
    print(f"  Created: sample_claims.csv")
    print(f"  Total claims: {len(df_demo)}")
    print(f"  Severity breakdown:")
    for severity, count in df_demo['actual_severity'].value_counts().items():
        pct = (count/len(df_demo))*100
        print(f"    {severity}: {count} ({pct:.1f}%)")
    print()
    
    # Generate larger datasets for batch testing
    sizes = {
        'small': 100,
        'medium': 500,
        'large': 1000,
        'xlarge': 2000
    }
    
    for name, size in sizes.items():
        print(f"Generating {name} dataset ({size} claims)...")
        df = generate_insurance_claims(size)
        filename = f'claims_{name}_{size}.csv'
        df.to_csv(filename, index=False)
        
        # Show statistics
        print(f"  Created: {filename}")
        print(f"  Total claims: {len(df)}")
        print(f"  Severity breakdown:")
        for severity, count in df['actual_severity'].value_counts().items():
            pct = (count/len(df))*100
            print(f"    {severity}: {count} ({pct:.1f}%)")
        print(f"  Date range: {df['filing_date'].min()} to {df['filing_date'].max()}")
        print()
    
    print("All datasets generated successfully!")