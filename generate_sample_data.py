import pandas as pd

# Sample insurance claims data
claims_data = {
    'claim_id': ['CLM001', 'CLM002', 'CLM003', 'CLM004', 'CLM005', 'CLM006'],
    'description': [
        "On March 15, 2024, my 2019 Honda Accord was rear-ended at the intersection of Main St and Oak Ave in Boston. The other driver ran a red light. Significant damage to rear bumper and trunk. Police report filed.",
        
        "Minor fender bender in parking lot on 01/20/2024. Small scratch on driver side door of my Toyota Camry. No injuries. Other party admitted fault.",
        
        "URGENT: My house at 123 Elm Street, Cambridge was severely damaged by fire on February 10th. Entire kitchen destroyed, smoke damage throughout second floor. Fire department report available. Estimated damage over $150,000.",
        
        "Windshield crack appeared suddenly while driving on highway yesterday. No accident, possibly hit by small rock. 2021 Tesla Model 3. Needs replacement.",
        
        "Claimed stolen vehicle from 456 Park Ave, Boston on 03/01/2024 but later found it in different parking lot where I forgot I parked it. False alarm, please disregard.",
        
        "Total loss - my 2018 Ford F-150 was completely submerged during flooding on River Road. Water damage to engine and interior. Vehicle is not drivable. Need immediate assistance."
    ],
    'actual_severity': ['High', 'Low', 'High', 'Low', 'Low', 'High']
}

df = pd.DataFrame(claims_data)
df.to_csv('sample_claims.csv', index=False)
print("Sample claims data generated successfully!")
print(f"Created {len(df)} sample claims in 'sample_claims.csv'")