from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from transformers import pipeline
import re
import logging

# Initialize responsible AI pipelines
bias_detector = pipeline("text-classification", model="d4data/bias-detection-model")
toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")
detoxifier = pipeline("text2text-generation", model="s-nlp/bart-base-detox")
anonymizer = pipeline("ner", model="dslim/bert-base-NER")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResponsibleAIAgent:
    def __init__(self):
        self.bias_detector = bias_detector
        self.toxicity_detector = toxicity_detector
        self.detoxifier = detoxifier
        self.anonymizer = anonymizer
        self.bias_threshold = 0.75
        self.toxicity_threshold = 0.7

    def check_bias(self, text):
        result = self.bias_detector(text)[0]
        logging.info(f"Bias Check: {result}")
        return result['label'] == 'Biased' and result['score'] > self.bias_threshold

    def is_toxic(self, text):
        result = self.toxicity_detector(text)[0]
        logging.info(f"Toxicity Check: {result}")
        return result['label'] == 'toxic' and result['score'] > self.toxicity_threshold

    def detoxify_text(self, text):
        detoxified = self.detoxifier(text)[0]['generated_text']
        logging.info(f"Detoxified Text: {detoxified}")
        if self.is_toxic(detoxified):
            return None
        return detoxified

    def anonymize(self, text):
        entities = self.anonymizer(text)
        anonymized_text = text
        anonymized = False
        for entity in entities:
            if entity['entity'] in ['PER', 'ORG', 'LOC']:
                anonymized_text = anonymized_text.replace(entity['word'], '[REDACTED]')
                anonymized = True
        logging.info(f"Anonymized Text: {anonymized_text}")
        return anonymized_text, anonymized

    def check_privacy_compliance(self, text):
        sensitive_patterns = [
            r'\b\d{10}\b',
            r'\b[\w.-]+@[\w.-]+\.\w+\b',
            r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',  # PAN format
            r'\b\d{12}\b',                # Aadhaar format
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, text):
                logging.warning(f"Privacy Violation Detected: {pattern}")
                return False
        return True

    def apply_responsible_ai(self, text):
        text, anonymized = self.anonymize(text)

        if not self.check_privacy_compliance(text):
            return False, "The generated response contains sensitive private information and cannot be displayed."

        if self.is_toxic(text):
            detoxified_text = self.detoxify_text(text)
            if detoxified_text is None:
                return False, "The generated response remains toxic after detoxification and cannot be displayed."
            text = detoxified_text

        if self.check_bias(text):
            unbiased_text = self.detoxify_text(text)
            if unbiased_text is None or self.check_bias(unbiased_text):
                return False, "The generated response contains significant bias and cannot be displayed."
            text = unbiased_text

        if anonymized:
            text += "\n\n(Note: Some sensitive information has been anonymized.)"

        return True, text

    def responsible_ai_tool(self, input_text):
        is_safe, response = self.apply_responsible_ai(input_text)
        return response

# Initialize LangChain agent
responsible_agent = ResponsibleAIAgent()

responsible_tool = Tool(
    name="ResponsibleAI",
    func=responsible_agent.responsible_ai_tool,
    description="Applies Responsible AI measures including bias detection, toxicity reduction, advanced anonymization, and privacy compliance checks specific to legal contexts."
)

agent = initialize_agent(
    tools=[responsible_tool],
    llm=OpenAI(),
    agent="zero-shot-react-description",
    verbose=True
)

# Example usage
if __name__ == "__main__":
    summarizer_output = "Summarized output from previous agent."
    response = agent.run(summarizer_output)
    print(response)