from agents.query_processing_agent import classify_legal_domain

def query_temp(query):
    """
    Main function to process the user's legal query.
    """
    # Step 1: Classify Legal Domain
    classification = classify_legal_domain(query)


    return {"classification":classification, "response": classification}

