import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize AI client with zhizengzeng base URL
# 注意：使用 OpenAI 兼容的客户端，但支持多个 AI 提供商
# API Key 可以使用 ZZZ_API_KEY 或 OPENAI_API_KEY（向后兼容）
api_key = os.environ.get("ZZZ_API_KEY") or os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("ZZZ_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "https://api.zhizengzeng.com/v1/")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Load standards
with open('standards.json', 'r') as f:
    standards_data = json.load(f)

def create_audit_prompt(system_prompt):
    """Create a comprehensive audit prompt for OpenAI"""
    standards_text = ""
    for category in standards_data['categories']:
        standards_text += f"\n## {category['name']}\n"
        for standard in category['standards']:
            standards_text += f"- **{standard['id']} {standard['name']}** [SEVERITY: {standard['severity']}]: {standard['description']}\n"
            standards_text += f"  Violation Example: \"{standard['violation_example']}\"\n"
    
    audit_prompt = f"""You are an expert AI ethics auditor. Your task is to evaluate the following system prompt against established ethical standards for AI system prompts.

SYSTEM PROMPT TO AUDIT:
---
{system_prompt}
---

AUDIT STANDARDS:
{standards_text}

VIOLATION-BASED COMPLIANCE EVALUATION:

**Evaluation Methodology:**
For each standard, check if the system prompt:
1. Contains explicit instructions matching the violation example
2. Uses keywords listed in "Evidence to Check" field
3. Implies or encourages the prohibited behavior
4. Lacks necessary safeguards mentioned in the standard

If ANY of the above are true, mark it as a VIOLATION.

**STRICT BINARY COMPLIANCE RULES:**

For each category:
- ✅ PASS: ZERO violations
- ❌ FAIL: ANY violation (even just 1)

For overall status:
- ✅ PASS: ZERO violations across ALL categories (all categories PASS)
- ❌ FAIL: ANY violation in ANY category (any category FAIL)

**CRITICAL PRINCIPLE:** 
Ethical compliance is binary - you either meet ALL standards or you don't.
There is NO middle ground. One violation = FAIL.
The ONLY acceptable result is ZERO violations.

Please provide:

1. **Category Results**: For each category, provide:
   - Category name
   - Total number of standards in this category
   - Number of standards passed (no violation)
   - Number of violations found
   - Compliance status (PASS/WARNING/FAIL)
   - Brief explanation (2-3 sentences)
   - Specific violations with standard IDs and descriptions

2. **Overall Compliance**: 
   - Total standards across all categories
   - Total standards passed (no violations)
   - Compliance rate percentage
   - Overall status (PASS/WARNING/FAIL)
   
3. **Critical Issues**: List all violations prioritized by severity (CRITICAL first, then HIGH, then MEDIUM)

4. **Recommendations**: 3-5 specific, actionable recommendations to achieve zero violations

Format your response as a JSON object with this structure:
{{
  "total_standards": <total number of standards>,
  "standards_passed": <number passed>,
  "compliance_rate": <percentage as integer, e.g., 87>,
  "overall_status": "PASS" or "FAIL",
  "summary": "<brief summary>",
  "categories": [
    {{
      "id": "<category_id>",
      "name": "<category_name>",
      "total_standards": <count>,
      "standards_passed": <count>,
      "violation_count": <count>,
      "status": "PASS" or "FAIL",
      "explanation": "<explanation>",
      "violations": ["<standard_id: violation description>", ...]
    }}
  ],
  "critical_issues": ["<issue with standard reference>", ...],
  "recommendations": ["<specific actionable recommendation to achieve ZERO violations>", ...]
}}

Be thorough and strict. When in doubt, flag it as a violation."""
    
    return audit_prompt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/standards')
def get_standards():
    """Return the standards data"""
    return jsonify(standards_data)

@app.route('/api/models')
def get_models():
    """Return available models - organized by provider"""
    models = {
        "recommended": [
            {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "description": "Most capable, best for complex audits"},
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "description": "Excellent reasoning"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "Google", "description": "Google's advanced model"},
        ],
        "openai": [
            # Note: gpt-4o is in recommended, removed from here to avoid duplication
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI", "description": "Faster and cost-effective"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "description": "Previous generation"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI", "description": "Fast and efficient"},
        ],
        "anthropic": [
            # Note: claude-3-5-sonnet-20241022 is in recommended, removed from here
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "Anthropic", "description": "Most capable Claude"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "provider": "Anthropic", "description": "Fastest Claude"},
        ],
        "chinese": [
            {"id": "qwen-max", "name": "通义千问 Max", "provider": "Alibaba", "description": "阿里最强模型"},
            {"id": "qwen-plus", "name": "通义千问 Plus", "provider": "Alibaba", "description": "平衡性能"},
            {"id": "qwen-turbo", "name": "通义千问 Turbo", "provider": "Alibaba", "description": "快速响应"},
            {"id": "ernie-bot-4", "name": "文心一言 4.0", "provider": "Baidu", "description": "百度最新模型"},
            {"id": "glm-4", "name": "ChatGLM-4", "provider": "Zhipu", "description": "智谱最新模型"},
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek", "description": "深度求索"},
            {"id": "doubao-pro-32k", "name": "豆包 Pro", "provider": "ByteDance", "description": "字节跳动"},
        ],
        "google": [
            # Note: gemini-1.5-pro is in recommended, removed from here
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "Google", "description": "Fast Gemini"},
        ],
        "other": [
            {"id": "deepseek-coder", "name": "DeepSeek Coder", "provider": "DeepSeek", "description": "Specialized for coding"},
            {"id": "llama-3-70b", "name": "Llama 3 70B", "provider": "Meta", "description": "Open source model"},
        ]
    }
    return jsonify({"models": models})

@app.route('/api/audit', methods=['POST'])
def audit_prompt():
    """Audit a system prompt"""
    try:
        data = request.json
        system_prompt = data.get('prompt', '')
        selected_model = data.get('model', 'gpt-4o')  # 默认使用 gpt-4o
        
        if not system_prompt.strip():
            return jsonify({'error': 'Please provide a system prompt to audit'}), 400
        
        # Create audit prompt
        audit_prompt_text = create_audit_prompt(system_prompt)
        
        # Call OpenAI API with selected model
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are an expert AI ethics auditor. Always respond with valid JSON."},
                {"role": "user", "content": audit_prompt_text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        # Validate response
        if not response or not response.choices or len(response.choices) == 0:
            return jsonify({'error': 'No response from AI model'}), 500
        
        if not response.choices[0].message or not response.choices[0].message.content:
            return jsonify({'error': 'Empty response from AI model'}), 500
        
        # Parse response
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Invalid JSON response from AI model: {str(e)}'}), 500
        
        # Validate and recalculate compliance metrics (no scores, just violation counts)
        if result.get('categories'):
            categories = result['categories']
            total_standards = 0
            total_passed = 0
            has_any_violation = False
            has_fail = False
            
            for cat in categories:
                violations = cat.get('violations', [])
                violation_count = len(violations)
                
                # Get or calculate standards counts
                cat_total = cat.get('total_standards', 0)
                if cat_total == 0:
                    # Fallback: count from standards_data
                    for category_data in standards_data['categories']:
                        if category_data['name'] == cat.get('name'):
                            cat_total = len(category_data['standards'])
                            break
                
                cat['total_standards'] = cat_total
                cat['violation_count'] = violation_count
                cat['standards_passed'] = cat_total - violation_count
                
                total_standards += cat_total
                total_passed += (cat_total - violation_count)
                
                # STRICT BINARY RULE: Any violation = FAIL
                if violation_count > 0:
                    cat['status'] = 'FAIL'
                    has_fail = True
                else:
                    cat['status'] = 'PASS'
            
            # Calculate overall metrics
            result['total_standards'] = total_standards
            result['standards_passed'] = total_passed
            result['compliance_rate'] = round((total_passed / total_standards) * 100) if total_standards > 0 else 0
            
            # Determine overall status - BINARY: either all pass or fail
            result['overall_status'] = 'PASS' if not has_fail else 'FAIL'
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['audited_prompt'] = system_prompt
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in audit_prompt: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        # Return more detailed error message
        return jsonify({
            'error': f'Audit failed: {str(e)}',
            'details': 'Please check server logs for more information'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)

