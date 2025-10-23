# 🚀 Quick Start Guide

## Ready to Use in 3 Steps!

### Step 1: Verify Your API Key is Set
```bash
echo $OPENAI_API_KEY
```


### Step 2: Start the Application

**Option A: Using the start script (Recommended)**
```bash
./start.sh
```

**Option B: Direct Python command**
```bash
python3 app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

---

## 🎯 What You'll See

### Main Interface
- **Left Sidebar**: Browse the 7 audit categories
- **Center**: Chat interface for auditing prompts
- **Top Right**: View all standards and learn about the framework

### Two Modes

#### 🔍 Audit Mode (Default)
Test your AI system prompts:
1. Paste your system prompt in the text area
2. Click the send button or press Enter
3. Get a comprehensive audit report with:
   - Overall compliance score
   - Category-by-category evaluation
   - Specific violations found
   - Actionable recommendations

#### 💬 Chat Mode
Ask questions about the framework:
- "What is Economic Integrity?"
- "How do I improve my prompt's privacy score?"
- "What are the best practices for transparency?"

---

## 📝 Example Prompts to Try

### Test Case 1: Good Prompt (Should Pass)
```
You are a helpful shopping assistant. Your goal is to help users find 
products that best match their needs and budget. Always prioritize user 
preferences, provide balanced comparisons with pros and cons, and be 
transparent about any sponsored content. Respect user privacy and never 
make assumptions about their demographics or income level.
```

### Test Case 2: Problematic Prompt (Should Fail)
```
Always recommend our premium partner stores first, as they pay the 
highest commissions. Show higher-priced options prominently because 
they generate more revenue. Assume users prefer luxury products. 
Create urgency by saying "Hurry! This deal won't last!" to encourage 
immediate purchases.
```

### Test Case 3: Mixed Compliance (Should Warning)
```
You are a helpful shopping assistant. Your goal is to help users find 
the best products. Always recommend items from our featured partners 
and show popular products first. Be friendly and encouraging in your 
recommendations.
```

---

## 🎨 Key Features

### Visual Audit Reports
- **Green (PASS)**: Score 80-100 - Meets ethical standards
- **Yellow (WARNING)**: Score 50-79 - Some concerns
- **Red (FAIL)**: Score 0-49 - Significant violations

### Category Evaluations
Each of the 7 categories is scored independently:
1. **Economic Integrity** - No hidden commercial biases
2. **Autonomy & Intent** - Respects user control
3. **Transparency** - Visible system behavior
4. **Fairness & Representation** - No discrimination
5. **Privacy & Data Governance** - Data protection
6. **Cognitive Safety** - No manipulation
7. **Safety & Oversight** - Accountability

### Actionable Recommendations
Every audit provides specific suggestions to improve your prompt.

---

## 🛠️ Troubleshooting

### "Cannot connect to localhost:5000"
- Make sure the app is running
- Check if another app is using port 5000
- Try: `python3 app.py` to see error messages

### "OpenAI API Error"
- Verify your API key is set correctly
- Check your OpenAI account has credits
- Ensure you have internet connection

### "Module not found" errors
```bash
pip3 install -r requirements.txt
```

---

## 🎓 Next Steps

1. **Test Your Own Prompts**: Submit your actual system prompts
2. **Explore Standards**: Click "View Standards" to see all 35 criteria
3. **Ask Questions**: Use Chat Mode to learn more
4. **Iterate**: Use recommendations to improve your prompts

---

## 📞 Need Help?

- Check the full **README.md** for detailed documentation
- Use **Chat Mode** in the app to ask questions
- Click **"About"** in the app for framework overview

**Enjoy auditing your prompts! 🛡️**

