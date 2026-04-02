import os
import re
import json
import urllib.request
from datetime import datetime

# Configuration
REPO = "yogender-ai/News-Intel-Feedback"
README_PATH = "README.md"
API_URL = f"https://api.github.com/repos/{REPO}/issues?state=open&labels=feedback&sort=created&direction=desc"

def get_issues():
    req = urllib.request.Request(API_URL, headers={"Accept": "application/vnd.github.v3+json"})
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data[:5] # Top 5 recent
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return []

def extract_metadata_from_body(body):
    # Fallback structure
    metadata = {"emotion": "💬", "rating": "⭐⭐⭐⭐⭐"}
    
    if not body:
        return metadata
        
    # Emotion mapping
    if "Type:" in body or "Emotion:" in body:
        lower_body = body.lower()
        if "praise" in lower_body or "positive" in lower_body: metadata["emotion"] = "💚"
        elif "bug" in lower_body or "negative" in lower_body: metadata["emotion"] = "🔴"
        elif "idea" in lower_body or "enhancement" in lower_body: metadata["emotion"] = "💡"
        
    # Rating extraction
    for line in body.split('\n'):
        if "Rating:" in line:
            stars = line.split(":")[-1].strip()
            # If stars is e.g. "5/5"
            try:
                rating = int(re.search(r'\d+', stars).group())
                metadata["rating"] = "⭐" * rating
            except:
                pass
                
    return metadata

def format_issues(issues):
    if not issues:
        return "*Awaiting fresh community feedback...*"
        
    html = []
    html.append("<table>")
    html.append("  <tr>")
    html.append("    <th width=\"15%\">User</th>")
    html.append("    <th width=\"10%\">Rating</th>")
    html.append("    <th width=\"10%\">Type</th>")
    html.append("    <th width=\"65%\">Feedback</th>")
    html.append("  </tr>")
    
    for issue in issues:
        author = issue['user']['login']
        # If the bot submitted it on behalf of someone, it's usually in the title or body
        title = issue['title']
        body = issue.get('body', '')
        
        # In our NewsIntel API, the title is usually: "Feedback from UserName"
        display_author = author
        if title.startswith("Feedback from "):
            display_author = title.replace("Feedback from ", "").strip()
        elif title.startswith("Idea from "):
            display_author = title.replace("Idea from ", "").strip()
        elif title.startswith("Issue from "):
            display_author = title.replace("Issue from ", "").strip()
            
        url = issue['html_url']
        metadata = extract_metadata_from_body(body)
        
        # Clean up body to a short message
        # Exclude the metadata block at the top if present
        clean_msg = ""
        for line in body.split('\n'):
            if line.strip() and not line.startswith("**") and not line.startswith("- "):
                clean_msg += line + " "
                if len(clean_msg) > 100:
                    clean_msg = clean_msg[:97] + "..."
                    break
        
        if not clean_msg:
            clean_msg = title
            
        html.append("  <tr>")
        html.append(f"    <td><strong>@{display_author}</strong></td>")
        html.append(f"    <td>{metadata['rating']}</td>")
        html.append(f"    <td align=\"center\">{metadata['emotion']}</td>")
        html.append(f"    <td>{clean_msg} <br/><a href=\"{url}\">View Thread &rarr;</a></td>")
        html.append("  </tr>")
        
    html.append("</table>")
    return "\n".join(html)

def update_readme(feedback_html):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_marker = "<!-- LIVE_FEEDBACK_START -->"
    end_marker = "<!-- LIVE_FEEDBACK_END -->"
    
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    
    if not pattern.search(content):
        print("Markers not found in README.md")
        return False
        
    new_content = pattern.sub(f"{start_marker}\n{feedback_html}\n{end_marker}", content)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    return True

if __name__ == "__main__":
    print("Fetching recent feedback...")
    issues = get_issues()
    print(f"Found {len(issues)} feedback issues.")
    
    html = format_issues(issues)
    
    print("Updating README.md...")
    success = update_readme(html)
    
    if success:
        print("README successfully updated!")
    else:
        print("Failed to update README.")
        exit(1)
