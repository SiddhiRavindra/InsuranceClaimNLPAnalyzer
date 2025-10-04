import spacy
from transformers import pipeline
import re
from datetime import datetime

# Load models - no auto-download needed
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class ClaimsAnalyzer:
    def __init__(self):
        self.fraud_keywords = [
            'stolen', 'theft', 'burglar', 'missing', 'disappeared',
            'false alarm', 'mistake', 'forgot', 'confused'
        ]
        self.severity_keywords = {
            'high': ['total loss', 'severe', 'destroyed', 'major', 'significant', 
                    'urgent', 'emergency', 'critical', 'extensive', 'complete'],
            'medium': ['moderate', 'damaged', 'broken', 'cracked', 'dented'],
            'low': ['minor', 'small', 'slight', 'scratch', 'chip', 'tiny']
        }
    
    def extract_entities(self, text):
        """Extract named entities from claim text"""
        doc = nlp(text)
        
        entities = {
            'locations': [],
            'dates': [],
            'money': [],
            'organizations': [],
            'vehicles': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'GPE' or ent.label_ == 'LOC':
                entities['locations'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['money'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
        
        # Extract vehicle information using regex
        vehicle_pattern = r'\b(19|20)\d{2}\s+[A-Z][a-z]+\s+[A-Z][a-z-]+\b'
        vehicles = re.findall(vehicle_pattern, text)
        entities['vehicles'] = vehicles
        
        return entities
    
    def classify_severity(self, text):
        """Classify claim severity based on keywords and sentiment"""
        text_lower = text.lower()
        
        # Count severity indicators
        high_count = sum(1 for keyword in self.severity_keywords['high'] 
                        if keyword in text_lower)
        medium_count = sum(1 for keyword in self.severity_keywords['medium'] 
                          if keyword in text_lower)
        low_count = sum(1 for keyword in self.severity_keywords['low'] 
                       if keyword in text_lower)
        
        # Get sentiment
        sentiment = sentiment_analyzer(text[:512])[0]
        
        # Decision logic
        if high_count >= 2 or (high_count >= 1 and sentiment['label'] == 'NEGATIVE'):
            severity = 'High'
            confidence = min(0.7 + (high_count * 0.1), 0.95)
        elif low_count >= 2 or (low_count >= 1 and sentiment['label'] == 'POSITIVE'):
            severity = 'Low'
            confidence = min(0.6 + (low_count * 0.1), 0.9)
        else:
            severity = 'Medium'
            confidence = 0.65
        
        return severity, confidence, sentiment
    
    def detect_fraud_indicators(self, text):
        """Detect potential fraud indicators"""
        text_lower = text.lower()
        
        indicators = []
        fraud_score = 0
        
        # Check for fraud keywords
        for keyword in self.fraud_keywords:
            if keyword in text_lower:
                indicators.append(f"Contains keyword: '{keyword}'")
                fraud_score += 1
        
        # Check for conflicting information
        if 'false alarm' in text_lower or 'mistake' in text_lower:
            indicators.append("Claim retraction mentioned")
            fraud_score += 2
        
        # Check for vague details
        if len(text.split()) < 20:
            indicators.append("Very short description (lack of detail)")
            fraud_score += 1
        
        # Check for excessive urgency
        urgency_words = ['urgent', 'immediately', 'asap', 'emergency']
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        if urgency_count >= 2:
            indicators.append("Excessive urgency language")
            fraud_score += 1
        
        fraud_risk = 'Low'
        if fraud_score >= 3:
            fraud_risk = 'High'
        elif fraud_score >= 2:
            fraud_risk = 'Medium'
        
        return fraud_risk, indicators, fraud_score
    
    def generate_summary(self, text):
        """Generate a brief summary of the claim"""
        doc = nlp(text)
        
        # Extract first sentence as summary
        sentences = list(doc.sents)
        if sentences:
            summary = str(sentences[0])
            # Limit to 100 characters
            if len(summary) > 100:
                summary = summary[:97] + "..."
            return summary
        return "No summary available"
    
    def analyze_claim(self, claim_text):
        """Complete analysis pipeline"""
        
        # Extract entities
        entities = self.extract_entities(claim_text)
        
        # Classify severity
        severity, confidence, sentiment = self.classify_severity(claim_text)
        
        # Detect fraud indicators
        fraud_risk, fraud_indicators, fraud_score = self.detect_fraud_indicators(claim_text)
        
        # Generate summary
        summary = self.generate_summary(claim_text)
        
        # Compile results
        results = {
            'summary': summary,
            'severity': severity,
            'severity_confidence': confidence,
            'sentiment': sentiment,
            'fraud_risk': fraud_risk,
            'fraud_indicators': fraud_indicators,
            'fraud_score': fraud_score,
            'entities': entities,
            'word_count': len(claim_text.split())
        }
        
        return results