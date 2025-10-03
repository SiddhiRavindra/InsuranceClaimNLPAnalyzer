import streamlit as st
import pandas as pd
from model import ClaimsAnalyzer
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Insurance Claims Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize analyzer
@st.cache_resource
def load_analyzer():
    return ClaimsAnalyzer()

try:
    analyzer = load_analyzer()
except Exception as e:
    st.error(f"Error loading analyzer: {e}")
    st.stop()

# Title and description
st.title("Insurance Claims Text Analyzer")
st.markdown("""
### AI-Powered Claims Processing for Liberty Mutual
This NLP system automatically analyzes insurance claim descriptions to:
- Classify claim severity
- Extract key information (dates, locations, vehicles, amounts)
- Detect potential fraud indicators
- Generate claim summaries

**Built for Solaria Labs Innovation Initiative**
""")

# Sidebar
st.sidebar.header("Analysis Options")
analysis_mode = st.sidebar.radio(
    "Select Mode:",
    ["Single Claim Analysis", "Batch Analysis", "Sample Claims Demo"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Use Cases
- Automated claim triage
- Fraud detection support
- Claims routing optimization
- Workload estimation
""")

# Main content based on mode
if analysis_mode == "Single Claim Analysis":
    st.header("Analyze Individual Claim")
    
    claim_text = st.text_area(
        "Enter claim description:",
        height=150,
        placeholder="On March 15, 2024, my 2019 Honda Accord was rear-ended..."
    )
    
    if st.button("Analyze Claim", type="primary"):
        if claim_text.strip():
            with st.spinner("Analyzing claim..."):
                try:
                    results = analyzer.analyze_claim(claim_text)
                    
                    # Display results in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Severity", results['severity'])
                        st.progress(results['severity_confidence'])
                        st.caption(f"Confidence: {results['severity_confidence']:.1%}")
                    
                    with col2:
                        st.metric("Fraud Risk", results['fraud_risk'])
                        fraud_indicator = {'Low': 'GREEN', 'Medium': 'YELLOW', 'High': 'RED'}
                        st.markdown(f"**Status: {fraud_indicator[results['fraud_risk']]}**")
                    
                    with col3:
                        st.metric("Word Count", results['word_count'])
                        sentiment_label = results['sentiment']['label']
                        st.markdown(f"**Sentiment: {sentiment_label}**")
                    
                    st.markdown("---")
                    
                    # Summary
                    st.subheader("Claim Summary")
                    st.info(results['summary'])
                    
                    # Entities
                    st.subheader("Extracted Information")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if results['entities']['locations']:
                            st.markdown("**Locations:**")
                            for loc in results['entities']['locations']:
                                st.markdown(f"- {loc}")
                        
                        if results['entities']['dates']:
                            st.markdown("**Dates:**")
                            for date in results['entities']['dates']:
                                st.markdown(f"- {date}")
                        
                        if results['entities']['money']:
                            st.markdown("**Amounts:**")
                            for money in results['entities']['money']:
                                st.markdown(f"- {money}")
                    
                    with col2:
                        if results['entities']['vehicles']:
                            st.markdown("**Vehicles:**")
                            for vehicle in results['entities']['vehicles']:
                                st.markdown(f"- {vehicle}")
                        
                        if results['entities']['organizations']:
                            st.markdown("**Organizations:**")
                            for org in results['entities']['organizations']:
                                st.markdown(f"- {org}")
                    
                    # Fraud indicators
                    if results['fraud_indicators']:
                        st.subheader("Fraud Indicators Detected")
                        for indicator in results['fraud_indicators']:
                            st.warning(indicator)
                    else:
                        st.success("No obvious fraud indicators detected")
                    
                    # Sentiment gauge
                    st.subheader("Sentiment Analysis")
                    sentiment_score = results['sentiment']['score']
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=sentiment_score * 100,
                        title={'text': f"Sentiment: {results['sentiment']['label']}"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 100], 'color': "gray"}
                            ]
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error analyzing claim: {e}")
        else:
            st.warning("Please enter a claim description to analyze.")

elif analysis_mode == "Batch Analysis":
    st.header("Batch Claims Analysis")
    
    uploaded_file = st.file_uploader("Upload CSV file with claims", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'description' in df.columns:
                st.success(f"Loaded {len(df)} claims")
                
                if st.button("Analyze All Claims", type="primary"):
                    with st.spinner("Analyzing claims..."):
                        results_list = []
                        
                        progress_bar = st.progress(0)
                        for idx, row in df.iterrows():
                            results = analyzer.analyze_claim(row['description'])
                            results['claim_id'] = row.get('claim_id', f'CLM{idx+1:03d}')
                            results_list.append(results)
                            progress_bar.progress((idx + 1) / len(df))
                        
                        # Create results dataframe
                        results_df = pd.DataFrame([
                            {
                                'Claim ID': r['claim_id'],
                                'Severity': r['severity'],
                                'Confidence': f"{r['severity_confidence']:.1%}",
                                'Fraud Risk': r['fraud_risk'],
                                'Summary': r['summary']
                            }
                            for r in results_list
                        ])
                        
                        st.subheader("Analysis Results")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Visualizations - FIXED VERSION
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Fixed: Create proper DataFrame for severity distribution
                            severity_data = [r['severity'] for r in results_list]
                            severity_df = pd.DataFrame({'Severity': severity_data})
                            severity_counts = severity_df['Severity'].value_counts()
                            
                            fig1 = px.pie(
                                values=severity_counts.values, 
                                names=severity_counts.index,
                                title="Severity Distribution"
                            )
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with col2:
                            # Fixed: Create proper DataFrame for fraud distribution
                            fraud_data = [r['fraud_risk'] for r in results_list]
                            fraud_df = pd.DataFrame({'Fraud Risk': fraud_data})
                            fraud_counts = fraud_df['Fraud Risk'].value_counts()
                            
                            fig2 = px.bar(
                                x=fraud_counts.index, 
                                y=fraud_counts.values,
                                title="Fraud Risk Distribution",
                                labels={'x': 'Risk Level', 'y': 'Count'}
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Results CSV",
                            data=csv,
                            file_name="claims_analysis_results.csv",
                            mime="text/csv"
                        )
            else:
                st.error("CSV must contain a 'description' column")
        except Exception as e:
            st.error(f"Error processing file: {e}")
            import traceback
            st.code(traceback.format_exc())

else:  # Sample Claims Demo
    st.header("Sample Claims Demo")
    
    try:
        df = pd.read_csv('sample_claims.csv')
        
        st.markdown("### Select a sample claim to analyze:")
        
        claim_options = [
            f"{row['claim_id']}: {row['description'][:80]}..." 
            for _, row in df.iterrows()
        ]
        selected_claim = st.selectbox("Choose claim:", claim_options)
        
        claim_idx = int(selected_claim.split(':')[0].replace('CLM', '')) - 1
        claim_text = df.iloc[claim_idx]['description']
        
        st.text_area("Full claim description:", claim_text, height=100, disabled=True)
        
        if st.button("Analyze This Claim", type="primary"):
            with st.spinner("Analyzing..."):
                try:
                    results = analyzer.analyze_claim(claim_text)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Severity", results['severity'])
                        if 'actual_severity' in df.columns:
                            actual = df.iloc[claim_idx]['actual_severity']
                            if results['severity'] == actual:
                                st.success(f"Matches actual: {actual}")
                            else:
                                st.warning(f"Actual: {actual}")
                    
                    with col2:
                        st.metric("Fraud Risk", results['fraud_risk'])
                    
                    with col3:
                        st.metric("Sentiment", results['sentiment']['label'])
                        st.caption(f"Score: {results['sentiment']['score']:.2f}")
                    
                    st.markdown("---")
                    st.subheader("Summary")
                    st.info(results['summary'])
                    
                    st.subheader("Extracted Information")
                    for key, values in results['entities'].items():
                        if values:
                            st.markdown(f"**{key.title()}:** {', '.join(values)}")
                    
                    if results['fraud_indicators']:
                        st.subheader("Fraud Indicators")
                        for indicator in results['fraud_indicators']:
                            st.warning(indicator)
                
                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    except FileNotFoundError:
        st.error("Sample data file not found. Please run: python generate_sample_data.py")
    except Exception as e:
        st.error(f"Error loading sample data: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built for Liberty Mutual Insurance - Solaria Labs Innovation Challenge</p>
    <p>Powered by spaCy, Transformers, and Streamlit</p>
</div>
""", unsafe_allow_html=True)