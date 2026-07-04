import os
import markdown

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
        
    # 遍歷 content 資料夾中的所有 markdown 檔案
    content_dir = 'content'
    if not os.path.exists(content_dir):
        print(f"錯誤：找不到內容資料夾 {content_dir}")
        return
        
    files = os.listdir(content_dir)
    md_files = [f for f in files if f.endswith('.md')]
    
    generated_pages = []
    
    for filename in md_files:
        filepath = os.path.join(content_dir, filename)
        
        # 讀取 Markdown 內容
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # 轉換為 HTML
        html_content = markdown.markdown(md_content)
        
        # 替換模板中的 {{content}} 占位符
        final_html = template_content.replace('{{content}}', html_content)
        
        # 決定輸出的 HTML 檔案名稱 (.md -> .html)
        out_filename = os.path.splitext(filename)[0] + '.html'
        out_filepath = os.path.join('public', out_filename)
        
        # 寫入至 public 資料夾
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        # 紀錄已生成的頁面，用於首頁清單 (可抓取檔名作為標題，或將來讀取 markdown 的第一個主標題)
        # 這裡簡單使用檔名（去掉副檔名）作為文章標題連結
        title = os.path.splitext(filename)[0]
        generated_pages.append({
            'title': title,
            'url': out_filename
        })
        
        print(f"成功生成文章：{out_filepath}")
        
    # 生成首頁 (index.html)
    index_links = []
    for page in generated_pages:
        index_links.append(f'<li><a href="{page["url"]}">{page["title"]}</a></li>')
    
    index_content = f"""<h1>文章列表</h1>
    <ul>
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