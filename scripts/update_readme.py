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
        
    # Emotion/Type extraction from body
    lower_body = body.lower()
    
    # Try table format first: | **Type** | Value |
    type_match = re.search(r'\*\*Type\*\*\s*\|\s*(.+?)\s*\|', body, re.IGNORECASE)
    if type_match:
        type_val = type_match.group(1).lower()
        if "praise" in type_val or "positive" in type_val: metadata["emotion"] = "💚"
        elif "bug" in type_val or "negative" in type_val: metadata["emotion"] = "🔴"
        elif "idea" in type_val or "enhancement" in type_val: metadata["emotion"] = "💡"
    elif "type:" in lower_body or "emotion:" in lower_body:
        # Fallback for old list format
        if "praise" in lower_body or "positive" in lower_body: metadata["emotion"] = "💚"
        elif "bug" in lower_body or "negative" in lower_body: metadata["emotion"] = "🔴"
        elif "idea" in lower_body or "enhancement" in lower_body: metadata["emotion"] = "💡"
        
    # Rating extraction
    # Try table format: | **Rating** | ⭐⭐⭐ (5/5) |
    rating_match = re.search(r'\*\*Rating\*\*\s*\|\s*(.+?)\s*\|', body)
    if rating_match:
        stars_line = rating_match.group(1)
        stars_count = stars_line.count("⭐")
        if stars_count > 0:
            metadata["rating"] = "⭐" * stars_count
    else:
        # Fallback for old list format
        for line in body.split('\n'):
            if "Rating:" in line:
                stars = line.split(":")[-1].strip()
                try:
                    rating = int(re.search(r'\d+', stars).group())
                    metadata["rating"] = "⭐" * rating
                except:
                    if "⭐" in stars:
                        metadata["rating"] = "⭐" * stars.count("⭐")
                break
                
    return metadata

def format_issues(issues):
    if not issues:
        return "<div align=\"center\">\n\n*Awaiting fresh community feedback...*\n\n</div>"
        
    html = []
    
    # ── Interactive Header ──
    html.append("<div align=\"center\">")
    html.append("  <a href=\"https://newsintel.yogender1.me/#feedback-section\">")
    html.append("    <img src=\"https://img.shields.io/badge/✨_Post_Feedback_Live-6366f1?style=for-the-badge&logo=rocket\" alt=\"Post Feedback\" />")
    html.append("  </a>")
    html.append("  &nbsp;")
    html.append("  <a href=\"https://github.com/yogender-ai/News-Intel-Feedback/issues\">")
    html.append("    <img src=\"https://img.shields.io/badge/💬_View_All_Discussions-0f0f23?style=for-the-badge&logo=github\" alt=\"View All\" />")
    html.append("  </a>")
    html.append("</div>")
    html.append("<br/>")
    
    html.append("<table width=\"100%\">")
    html.append("  <tr style=\"background: rgba(99, 102, 241, 0.1);\">")
    html.append("    <th width=\"20%\" align=\"left\">👤 User</th>")
    html.append("    <th width=\"15%\" align=\"center\">⭐ Rating</th>")
    html.append("    <th width=\"12%\" align=\"center\">🏷️ Type</th>")
    html.append("    <th width=\"53%\" align=\"left\">💬 Feedback Message</th>")
    html.append("  </tr>")
    
    for issue in issues:
        author = issue['user']['login']
        title = issue['title']
        body = issue.get('body', '')
        
        # --- Advanced Author Extraction ---
        display_author = author
        
        # 1. Try body table: **Author** | name |
        author_match = re.search(r'\*\*Author\*\*\s*\|\s*(.+?)\s*\|', body)
        if author_match:
            display_author = author_match.group(1).strip()
        else:
            # 2. Try body list: **Author:** name
            author_match = re.search(r'\*\*Author:\*\*\s*(.+)', body)
            if author_match:
                display_author = author_match.group(1).strip()
            else:
                # 3. Try title: "Feedback from Name" (ignoring emojis)
                title_match = re.search(r'Feedback from\s+(.+?)(?:\s+—|$)', title)
                if title_match:
                    display_author = title_match.group(1).strip()
                elif " from " in title:
                    # Fallback for "Idea from Name", "Issue from Name"
                    display_author = title.split(" from ")[-1].split("—")[0].strip()
        
        # Remove any @ from display_author to avoid double @@
        display_author = display_author.replace('@', '')
            
        url = issue['html_url']
        metadata = extract_metadata_from_body(body)
        
        # Robust message extraction
        clean_msg = ""
        # Look for the message between "### Message" and the footer line "---"
        msg_parts = re.split(r'### Message', body)
        if len(msg_parts) > 1:
            msg_content = msg_parts[1].split('---')[0].strip()
            clean_msg = msg_content
        else:
            # Fallback: find any text that isn't a table or header
            lines = [l.strip() for l in body.split('\n') if l.strip() and not re.match(r'^(#|\||\*\*|- )', l)]
            clean_msg = " ".join(lines)
        
        if not clean_msg:
            clean_msg = title
            
        # Truncate and clean
        if len(clean_msg) > 160:
            clean_msg = clean_msg[:157] + "..."
        clean_msg = clean_msg.replace('\n', ' ').strip()
        
        # Determine badge color based on emotion
        colors = {"💚": "10b981", "💡": "f59e0b", "🔴": "f43f5e", "💬": "6366f1"}
        color = colors.get(metadata['emotion'], "6366f1")
        type_label = "Feedback"
        if metadata['emotion'] == "💚": type_label = "Praise"
        elif metadata['emotion'] == "💡": type_label = "Idea"
        elif metadata['emotion'] == "🔴": type_label = "Bug"
            
        html.append("  <tr>")
        html.append(f"    <td><strong><a href=\"https://github.com/{author}\">@{display_author}</a></strong></td>")
        html.append(f"    <td align=\"center\"><code style=\"color: #f59e0b;\">{metadata['rating']}</code></td>")
        html.append(f"    <td align=\"center\"><img src=\"https://img.shields.io/badge/-{type_label}-{color}?style=flat-square\" alt=\"{type_label}\" /></td>")
        html.append(f"    <td><em>\"{clean_msg}\"</em> <br/><small><a href=\"{url}\">View Context &rarr;</a></small></td>")
        html.append("  </tr>")
        
    html.append("</table>")
    
    # ── Footer Stats ──
    now = datetime.utcnow().strftime("%b %d, %H:%M UTC")
    html.append("<br/>")
    html.append("<div align=\"center\">")
    html.append(f"  <img src=\"https://img.shields.io/badge/Sync_Status-Live-10b981?style=flat-square&logo=github-actions\" />")
    html.append(f"  &nbsp; <img src=\"https://img.shields.io/badge/Last_Sync-{now.replace(' ', '_')}-6366f1?style=flat-square\" />")
    html.append("</div>")
    
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
    
    # Also update the 'stars' badge if we want to be fancy
    # But for now let's just do the feedback
    
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
