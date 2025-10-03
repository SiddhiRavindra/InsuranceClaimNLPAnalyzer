print("Testing imports...")

try:
    import spacy
    print("✓ spacy imported")
except Exception as e:
    print(f"✗ spacy error: {e}")

try:
    from transformers import pipeline
    print("✓ transformers imported")
except Exception as e:
    print(f"✗ transformers error: {e}")

try:
    import streamlit
    print("✓ streamlit imported")
except Exception as e:
    print(f"✗ streamlit error: {e}")

try:
    import pandas
    print("✓ pandas imported")
except Exception as e:
    print(f"✗ pandas error: {e}")

try:
    import plotly
    print("✓ plotly imported")
except Exception as e:
    print(f"✗ plotly error: {e}")

print("\nTesting model.py...")

try:
    from model import ClaimsAnalyzer
    print("✓ model.py imported")
    
    analyzer = ClaimsAnalyzer()
    print("✓ ClaimsAnalyzer created")
    
    test_claim = "My car was damaged in an accident."
    result = analyzer.analyze_claim(test_claim)
    print("✓ analyze_claim works")
    print(f"  Severity: {result['severity']}")
    print(f"  Fraud Risk: {result['fraud_risk']}")
except Exception as e:
    print(f"✗ model error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete!")