import ast
import json

def extract_content_key(pipe_delimited_line):
    """Extract the 'content' value from a pipe-delimited CSV line"""
    
    # Split the line by pipe delimiter
    fields = pipe_delimited_line.split('|')
    
    # The last field contains the JSON-like dictionary
    json_field = fields[-1]
    
    try:
        # First try to parse as JSON
        data_dict = json.loads(json_field)
    except json.JSONDecodeError:
        try:
            # If JSON fails, try ast.literal_eval (handles Python dict format)
            data_dict = ast.literal_eval(json_field)
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing data: {e}")
            return None
    
    # Extract the content value
    content = data_dict.get('content', '')
    return content

def extract_content_key_safe(pipe_delimited_line):
    """Safer version with more error handling"""
    
    try:
        fields = pipe_delimited_line.split('|')
        if len(fields) < 8:  # Based on your example, should have 8 fields
            print(f"Warning: Expected at least 8 fields, got {len(fields)}")
        
        json_field = fields[-1].strip()
        
        # Try both JSON and literal_eval
        for parser in [json.loads, ast.literal_eval]:
            try:
                data_dict = parser(json_field)
                content = data_dict.get('content', '')
                return content
            except:
                continue
        
        print("Could not parse the data dictionary")
        return None
        
    except Exception as e:
        print(f"Error processing line: {e}")
        return None

# Test with your example line
sample_line = """2025-07-22-17-43-57|ARTICLE_WRITER|TRANSLATE|gpt-4o-mini|0|AI Agent Memory Systems: Making Machines Remember|0.80|{'content': 'Systèmes de Mémoire des Agents IA : Faire en Sorte que les Machines se Souviennent', 'additional_kwargs': {'refusal': None}, 'response_metadata': {'token_usage': {'completion_tokens': 20, 'prompt_tokens': 46, 'total_tokens': 66, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': None, 'id': 'chatcmpl-BwANn8lluiAoRWsL92Rl1yXs2jImK', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, 'type': 'ai', 'name': None, 'id': 'run--a61fddb3-1a4f-4ec3-a20e-71a3f77d7538-0', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': {'input_tokens': 46, 'output_tokens': 20, 'total_tokens': 66, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}}"""

print("Testing content extraction:")
print("="*50)

# Method 1: Basic extraction
content = extract_content_key(sample_line)
print(f"Extracted content: {content}")

print("\n" + "="*50)

# Method 2: Safe extraction
content_safe = extract_content_key_safe(sample_line)
print(f"Extracted content (safe): {content_safe}")

print("\n" + "="*50)

# Show all fields for context
fields = sample_line.split('|')
print("All fields in the line:")
for i, field in enumerate(fields):
    if i == len(fields) - 1:  # Last field (the dictionary)
        print(f"Field {i}: [DICTIONARY DATA - contains content key]")
    else:
        print(f"Field {i}: {field}")

print(f"\nField positions:")
print(f"0: Timestamp")
print(f"1: ARTICLE_WRITER") 
print(f"2: TRANSLATE")
print(f"3: Model (gpt-4o-mini)")
print(f"4: Some number (0)")
print(f"5: Title")
print(f"6: Score (0.80)")
print(f"7: Dictionary with content key")

# For processing multiple lines from a file
def process_csv_file(filename):
    """Process entire CSV file and extract all content keys"""
    content_list = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
                
            content = extract_content_key_safe(line)
            if content:
                content_list.append(content)
            else:
                print(f"Warning: Could not extract content from line {line_num}")
    
    return content_list

# Example usage for file processing:
print(f"\n" + "="*50)
print("For processing a full CSV file:")
print("# Usage example:")
print("# content_keys = process_csv_file('your_file.csv')")
print("# for i, content in enumerate(content_keys):")
print("#     print(f'{i+1}: {content}')")
