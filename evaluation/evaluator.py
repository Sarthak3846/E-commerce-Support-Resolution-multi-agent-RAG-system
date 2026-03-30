import sys
import os
import json
import time

# Ensure the app modules can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.orchestrator import run_ticket_resolution

TEST_FILE = "evaluation/test_cases.json"

def load_tests():
    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(f"Test cases file not found at {TEST_FILE}.")
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate():
    tests = load_tests()
    total = len(tests)
    correct = 0

    # Define our classes for tracking metrics
    classes = ["approve", "deny", "partial", "needs escalation"]
    
    # True Positives, False Positives, False Negatives for Precision/Recall
    tp = {c: 0 for c in classes}
    fp = {c: 0 for c in classes}
    fn = {c: 0 for c in classes}

    print(f"Running evaluation on {total} test cases...\n")

    for i, test in enumerate(tests):
        ticket = test["ticket"]
        context = test["order_context"]
        expected = test.get("expected_decision", "unknown").lower()

        # Run the pipeline safely
        try:
            output, _ = run_ticket_resolution(ticket, context)
            
            # Check if the API failed with Max Retries
            if output.get("error") == "Max retries exceeded" or output.get("rationale") == "Missing citations":
                predicted = "api_error"
            else:
                predicted = output.get("decision")
                if predicted is None:
                    predicted = "unknown"
                predicted = str(predicted).lower()
                
        except Exception as e:
            predicted = "error"
            print(f"  [ERROR] Script failed on Test {i+1}: {e}")

        # 1. Simple Comparison
        is_correct = (predicted == expected)

        if is_correct:
            correct += 1
            if expected in tp:
                tp[expected] += 1
        else:
            if predicted in fp:
                fp[predicted] += 1
            if expected in fn:
                fn[expected] += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"Test {i+1}/{total} | Expected: '{expected}' | Predicted: '{predicted}' -> [{status}]")
        
        # ADDED DELAY TO PREVENT "MAX RETRIES EXCEEDED" RATE LIMITS
        time.sleep(3)

    # 2. Calculate Overall Metrics
    accuracy = correct / total if total > 0 else 0
    pass_at_1 = accuracy # Pass@k where k=1 is identical to Accuracy for single-generation tasks

    print("\n" + "="*40)
    print("EVALUATION METRICS")
    print("="*40)
    print(f"Accuracy:  {accuracy*100:.2f}% ({correct}/{total})")
    print(f"Pass@1:    {pass_at_1*100:.2f}%")
    
    # 3. Calculate Precision & Recall per class
    print("\nClass-wise Metrics:")
    macro_p = 0
    macro_r = 0
    valid_classes = 0

    for c in classes:
        p_den = tp[c] + fp[c]
        r_den = tp[c] + fn[c]
        
        precision = tp[c] / p_den if p_den > 0 else 0.0
        recall = tp[c] / r_den if r_den > 0 else 0.0

        print(f"  - {c.upper()}:")
        print(f"      Precision: {precision*100:.2f}%")
        print(f"      Recall:    {recall*100:.2f}%")
        
        # Only include classes that actually existed in the test set for the Macro Average
        if r_den > 0: 
            macro_p += precision
            macro_r += recall
            valid_classes += 1

    if valid_classes > 0:
        print(f"\nMacro-Average Precision: {(macro_p/valid_classes)*100:.2f}%")
        print(f"Macro-Average Recall:    {(macro_r/valid_classes)*100:.2f}%")
    print("="*40)

if __name__ == "__main__":
    evaluate()