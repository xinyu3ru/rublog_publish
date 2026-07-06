// 在解析文章时提取分类和标签
const articles = lines.map(line => {
  const match = line.match(
    /^\[(.+?)\]\((.+?)\)(?:&emsp;|&nbsp;|\s)+发布时间：\s*([\d-]+)/
  );
  if (!match) return null;

  const [, title, url, datetime] = match;
  const slug = generateSlug(title, url);
  
  // 从URL推断分类（示例逻辑，需要根据你的实际URL结构调整）
  let categories = ['software']; // 默认分类
  if (url.includes('/hardware/')) categories = ['hardware'];
  if (url.includes('/network/')) categories = ['network'];
  
  return {
    title: title.trim(),
    url: url.trim(),
    date: datetime.replace(/-(\d{2}):(\d{2})$/, ''),
    datetime: datetime.trim(),
    slug,
    categories,
    tags: extractTagsFromTitle(title) // 从标题提取标签
  };
}).filter(Boolean);

function extractTagsFromTitle(title: string): string[] {
  const tagKeywords = {
    'plc': ['plc', '西门子', 'smart', 'wincc'],
    'modbus': ['modbus', 'rtu'],
    'linux': ['linux', 'ubuntu', 'shell'],
    'windows': ['windows', 'win'],
    'network': ['network', 'grafana', 'ssh'],
    'tools': ['工具', 'pdf', 'putty', 'zsh']
  };
  
  const lowerTitle = title.toLowerCase();
  const tags: string[] = [];
  
  for (const [tag, keywords] of Object.entries(tagKeywords)) {
    if (keywords.some(keyword => lowerTitle.includes(keyword))) {
      tags.push(tag);
    }
  }
  
  return tags.length > 0 ? tags : ['uncategorized'];
}