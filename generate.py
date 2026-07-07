import os
import re
from datetime import datetime
import markdown

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = os.path.splitext(os.path.basename(filepath))[0]
    # 預設日期為檔案修改時間
    mtime = os.path.getmtime(filepath)
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    
    markdown_body = content
    
    # 1. 嘗試解析 YAML Front Matter (例如最開頭的 --- 區塊)
    front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if front_matter_match:
        front_matter = front_matter_match.group(1)
        markdown_body = content[front_matter_match.end():]
        for line in front_matter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key == 'title':
                    title = value.strip('"\'')
                elif key == 'date':
                    date_str = value.strip('"\'')
    else:
        # 2. 如果沒有 Front Matter，尋找第一個 # 標題作為文章標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            
        # 3. 尋找內文中的 Date: 或 日期: 標籤
        date_match = re.search(r'^(?:Date|date|日期)\s*:\s*([\d\-/]+)', content, re.MULTILINE)
        if date_match:
            date_str = date_match.group(1).strip()

    return title, date_str, markdown_body

def generate_site():
    # 確保輸出資料夾存在
    os.makedirs('public', exist_ok=True)
    
    # 讀取 base.html 模板
    template_path = os.path.join('templates', 'base.html')
    if not os.path.exists(template_path):
        print(f"錯誤：找不到模板檔案 {template_path}")
        return
        
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
        
    content_dir = 'content'
    if not os.path.exists(content_dir):
        print(f"錯誤：找不到內容資料夾 {content_dir}")
        return
        
    # 遞迴掃描 content 資料夾內所有的 .md 檔案
    md_files = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    generated_pages = []
    
    for filepath in md_files:
        # 取得相對路徑以保持結構（若未來有子資料夾）
        rel_path = os.path.relpath(filepath, content_dir)
        out_rel_html = os.path.splitext(rel_path)[0] + '.html'
        out_filepath = os.path.join('public', out_rel_html)
        
        # 確保輸出的子資料夾存在
        os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
        
        # 解析 Markdown 檔案
        title, date_str, markdown_body = parse_markdown(filepath)
        
        # 轉換為 HTML
        html_content = markdown.markdown(markdown_body)
        
        # 替換模板中的 {{content}} 占位符
        final_html = template_content.replace('{{content}}', html_content)
        
        # 寫入至 public 資料夾
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        # 紀錄已生成的頁面資訊，用於首頁清單
        # 將來超連結要使用對應的相對路徑
        generated_pages.append({
            'title': title,
            'date': date_str,
            'url': out_rel_html.replace('\\', '/')
        })
        
        print(f"成功生成文章：{out_filepath} (標題: {title}, 日期: {date_str})")
        
    # 依照日期降序排列文章 (最新的在前面)
    generated_pages.sort(key=lambda x: x['date'], reverse=True)
    
    # 生成首頁內容
    index_links = []
    for page in generated_pages:
        index_links.append(f'<li><span class="post-date">[{page["date"]}]</span> <a href="{page["url"]}">{page["title"]}</a></li>')
    
    index_content = f"""<h1>文章列表</h1>
    <ul class="post-list">
        {"\n        ".join(index_links)}
    </ul>"""
    
    # 使用 base.html 模板來包裝首頁內容
    index_html = template_content.replace('{{content}}', index_content)
    index_filepath = os.path.join('public', 'index.html')
    
    with open(index_filepath, 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print(f"成功生成首頁：{index_filepath}")

if __name__ == '__main__':
    generate_site()