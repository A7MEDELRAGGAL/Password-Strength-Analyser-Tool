import hashlib
import os
import re

# ==========================================
# Project: Password Analyser & Cracking Tool
# Team: Ships Group
# Leader: Ahmed Mohammed Saad El-Raggal (ID: 2221300)
# Description: CLI tool for password strength analysis and secure hashing.
# ==========================================

def analyze_strength(password):
    """
    Evaluates password complexity based on length, digits, uppercase, and symbols.
    Returns: Strength Level & Feedback list.
    """
    score = 0
    feedback = []
    
    # 1. Check Length
    if len(password) >= 8: score += 1
    else: feedback.append("- Length is too short (must be 8+ chars)")

    # 2. Check Digits
    if re.search(r"\d", password): score += 1
    else: feedback.append("- Missing numbers (0-9)")

    # 3. Check Uppercase
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("- Missing uppercase letters (A-Z)")

    # 4. Check Special Characters
    if re.search(r"[!@#$%^&*]", password): score += 1
    else: feedback.append("- Missing symbols (!@#$)")

    # Result Logic
    if score < 2: return "WEAK", feedback
    elif score < 4: return "MEDIUM", feedback
    else: return "STRONG", feedback

def secure_storage_simulation(password):
    """
    Simulates secure database storage using Salt + SHA-256.
    """
    # Step A: Generate Random Salt (16 bytes)
    salt = os.urandom(16).hex()
    
    # Step B: Combine Salt and Password
    combined = salt + password
    
    # Step C: Hash the combination
    final_hash = hashlib.sha256(combined.encode()).hexdigest()
    
    return salt, final_hash

def main():
    print(f"{'='*60}")
    print(f" PASSWORD ANALYSER & SECURE STORAGE TOOL")
    print(f" Developed by: Ahmed El-Raggal | ID: 2221300")
    print(f"{'='*60}\n")

    while True:
        pwd = input(">> Enter password to test (or 'q' to quit): ")
        if pwd.lower() == 'q': break
        
        print("\n--- [1] Analysis Report ---")
        strength, tips = analyze_strength(pwd)
        print(f" Strength: {strength}")
        if tips:
            print(" Recommendations:")
            for tip in tips: print(f"   {tip}")

        print("\n--- [2] Secure Storage Simulation ---")
        salt, hashed = secure_storage_simulation(pwd)
        print(f" [Salt]: {salt}")
        print(f" [Hash]: {hashed}")
        
        print(f"\n{'-'*60}\n")

if __name__ == "__main__":
    main()