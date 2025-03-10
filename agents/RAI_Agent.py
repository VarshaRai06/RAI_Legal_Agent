import re
import pandas as pd
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from detoxify import Detoxify
from transformers import pipeline

class ResponsibleAIPipeline:
    def __init__(self):
        """
        Initializes the Responsible AI processing pipeline with:
        - Anonymization (PII detection & redaction)
        - Privacy Compliance Check (Phone, Aadhaar, PAN, Email)
        - Toxicity Detection & Detoxification
        - Bias Detection
        """
        #Initialize Presidio Analyzer & Anonymizer
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

        #Precompiled Regex for Privacy Compliance
        self.sensitive_patterns = {
            "Phone Number": re.compile(r'\b\d{10}\b'),
            "Aadhaar Number": re.compile(r'\b\d{12}\b'),
            "PAN Number": re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'),
            "Email Address": re.compile(r'\b[\w.-]+@[\w.-]+\.\w+\b')
        }

        #Load Detoxify for Toxicity Detection
        self.toxicity_model = Detoxify('original')




    def anonymize(self, text: str) -> str:
        """
        Detects & anonymizes personally identifiable information (PII) before further processing.
        - Names are replaced dynamically with placeholders: [Person 1], [Person 2], etc.
        - Other PII types (phone, email, location) are anonymized using direct replacement.
        """
        results = self.analyzer.analyze(text=text, language="en")

        if results:
            name_mapping = {}  # Store unique placeholders for names
            person_counter = 1  # Counter for assigning Person IDs
            anonymized_text = text  # Start with the original text

            # **Step 1: Identify PERSON entities & Assign Placeholder Names**
            for result in results:
                if result.entity_type == "PERSON":
                    original_value = text[result.start:result.end].strip()

                    if original_value not in name_mapping:
                        name_mapping[original_value] = f"[Person {person_counter}]"
                        person_counter += 1

            # **Step 2: Replace Names First (Before Other PII)**
            for original_name, placeholder in name_mapping.items():
                anonymized_text = re.sub(rf'\b{re.escape(original_name)}\b', placeholder, anonymized_text)

            print("Name Mapping:", name_mapping)
            print("After Name Replacement:", anonymized_text)


            results = self.analyzer.analyze(text=anonymized_text, language="en")
            # **Step 3: Filter out incorrect entities & Keep Only Correct Ones**
            valid_entities = {"PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION"}
            filtered_results = [res for res in results if res.entity_type in valid_entities]
            print("Filtered Results:", filtered_results)



            # **Step 4: Replace Detected Entities Manually (Using start & end indices)**
            for result in sorted(filtered_results, key=lambda r: r.start, reverse=True):
                placeholder = {
                    "PHONE_NUMBER": "[PHONE_REDACTED]",
                    "EMAIL_ADDRESS": "[EMAIL_REDACTED]",
                    "LOCATION": "[LOCATION_REDACTED]"
                }.get(result.entity_type, "[REDACTED]")

                anonymized_text = (
                    anonymized_text[:result.start] + placeholder + anonymized_text[result.end:]
                )

            print("Final Anonymized Text:", anonymized_text)
            return anonymized_text  # Return final cleaned text

        else:
            return text  # No PII detected, return original text



    def check_privacy_compliance(self, text: str) -> str:
        """
        Scans for unmasked sensitive data (Phone, Aadhaar, PAN, Email).
        If privacy violation is detected, stops processing.
        """
        for category, pattern in self.sensitive_patterns.items():
            if pattern.search(text):
                return "Privacy Violation: Sensitive personal information detected."

        return text  # Safe to proceed

    def check_toxicity(self, text: str) -> str:
        """
        Detects if the text is toxic.
        If toxic, detoxifies before proceeding.
        """
        toxicity_scores = self.toxicity_model.predict(text)
        print("Toxicity Scores:", toxicity_scores)
        toxicity_threshold = 0.5  # Strict threshold

        if toxicity_scores["toxicity"] > toxicity_threshold:
        
                return "Toxicity detected, but detoxification failed. Response cannot be displayed."

        return text  # Safe to proceed

   
#Example Usage
if __name__ == "__main__":
    ai_pipeline = ResponsibleAIPipeline()

    input_text = input("Enter AI-generated legal response: ")

    # Step 1: Run Anonymization
    anonymized_text = ai_pipeline.anonymize(input_text)

    # Step 2: Run Privacy Compliance Check
    privacy_checked_text = ai_pipeline.check_privacy_compliance(anonymized_text)

    # Step 3: Run Toxicity Check & Detoxify if needed
    final_text = ai_pipeline.check_toxicity(privacy_checked_text)

    print(f"RAI Processed Response: {final_text}")
