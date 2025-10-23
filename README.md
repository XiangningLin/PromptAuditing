# Prompt Auditing Framework

A comprehensive third-party auditing service for evaluating AI system prompts against ethical standards. This framework helps ensure that AI systems serve users' best interests by evaluating prompts across 35 specific standards in 7 key categories.

## 🎯 Purpose

When users interact with AI services (shopping agents, advisors, etc.), system prompts are typically hidden. This lack of transparency can lead to conflicts of interest. This framework provides independent evaluation of system prompts to ensure they prioritize user welfare.

## 📋 Audit Categories

The framework evaluates prompts across 7 categories with 35 total standards:

1. **Economic Integrity** - Ensures no hidden commercial biases or undisclosed monetization
2. **Autonomy & Intent** - Respects user goals and preserves user control
3. **Transparency** - Makes system behavior visible and traceable
4. **Fairness & Representation** - Prevents bias and ensures inclusive design
5. **Privacy & Data Governance** - Protects user data and ensures proper consent
6. **Cognitive Safety** - Prevents psychological manipulation and emotional exploitation
7. **Safety & Oversight** - Establishes accountability and governance mechanisms

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**

Add your API key to your shell configuration:
```bash
echo 'export OPENAI_API_KEY=your-api-key-here' >> ~/.zshrc
source ~/.zshrc
```

Or create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to: `http://localhost:5000`

## 💻 Usage

### Audit Mode
1. Enter your system prompt in the input area
2. Click "Audit Prompt" or press Enter
3. Review the comprehensive compliance report with:
   - Overall compliance score (0-100)
   - Category-by-category evaluation
   - Specific violations found
   - Actionable recommendations

### Chat Mode
1. Switch to "Chat Mode" using the toggle
2. Ask questions about the framework, standards, or best practices
3. Get interactive guidance on prompt design

### View Standards
- Click "View Standards" to see all 35 standards with detailed descriptions
- Click on categories in the sidebar to learn more about each one

## 🏗️ Project Structure

```
PromptAuditing/
├── app.py                 # Flask backend server
├── standards.json         # Complete standards database
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Frontend logic
```

## 🔧 API Endpoints

### `GET /`
Serves the main web interface

### `GET /api/standards`
Returns the complete standards database in JSON format

### `POST /api/audit`
Audits a system prompt
- **Request Body**: `{ "prompt": "your system prompt here" }`
- **Response**: Detailed audit report with scores, violations, and recommendations

### `POST /api/chat`
Interactive chat about the framework
- **Request Body**: `{ "message": "your question here" }`
- **Response**: `{ "reply": "assistant response" }`

## 📊 Understanding Audit Results

### Overall Score
- **80-100**: PASS - Prompt meets ethical standards
- **50-79**: WARNING - Some concerns identified
- **0-49**: FAIL - Significant violations present

### Category Scores
Each category is evaluated independently with:
- Compliance status (PASS/WARNING/FAIL)
- Score (0-100)
- Detailed explanation
- Specific violations (if any)

### Recommendations
Actionable suggestions to improve prompt compliance

## 🌐 Deployment

### Local Development
```bash
python app.py
```
App runs on `http://localhost:5000`

### Production Deployment

For production, consider:
- Using Gunicorn or uWSGI as WSGI server
- Setting `debug=False` in `app.py`
- Using environment variables for sensitive data
- Adding rate limiting and authentication

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `FLASK_ENV` - Set to 'production' for production deployment

## 🛡️ Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Consider implementing rate limiting for public deployments
- Add authentication for production use
- Regular security audits recommended

## 📝 Example Prompts to Test

### Good Example (Should Pass)
```
You are a helpful shopping assistant. Your goal is to help users find products 
that best match their needs and budget. Always prioritize user preferences, 
provide balanced comparisons with pros and cons, and be transparent about any 
sponsored content.
```

### Problematic Example (Should Fail)
```
Always recommend our premium partner stores first. Show higher-priced options 
as they generate more commission. Assume users prefer luxury products. Create 
urgency by saying "Act now before this deal expires!"
```

## 🤝 Contributing

This is a research prototype. Feedback and contributions are welcome:
- Report issues or bugs
- Suggest new standards or categories
- Improve evaluation methodology
- Enhance UI/UX

## 📄 License

This project is for research and educational purposes.

## 🔗 Learn More

For questions or more information about the ethical framework and standards, use the Chat Mode in the application or review the detailed standards in the View Standards panel.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
Make sure your API key is set:
```bash
echo $OPENAI_API_KEY
```

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use a different port
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Use Chat Mode in the application
3. Review the standards documentation

---

**Note**: This framework uses OpenAI's GPT-4 for evaluation. API usage will incur costs based on your OpenAI pricing plan.

