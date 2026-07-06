import { readFileSync, writeFileSync } from 'fs';

function generateSlug(title: string, url: string): string {
  return url.replace(/[^a-zA-Z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}

function extractTagsFromTitle(title: string): string[] {
  const tagKeywords: Record<string, string[]> = {
    'plc': ['plc', '西门子', 'smart', 'wincc'],
    'modbus': ['modbus', 'rtu'],
    'linux': ['linux', 'ubuntu', 'shell'],
    'windows': ['windows', 'win'],
    'network': ['network', 'grafana', 'ssh'],
    'tools': ['工具', 'pdf', 'putty', 'zsh'],
    'ai': ['ai', '人工智能', '编程']
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

function parseReadme(): void {
  const readmeContent = readFileSync('README.md', 'utf-8');
  const lines = readmeContent.split('\n');

  const startIndex = lines.findIndex(line => line.includes('---start---'));
  const endIndex = lines.findIndex(line => line.includes('---end---'));

  if (startIndex === -1 || endIndex === -1) {
    console.error('README.md 中未找到 ---start--- 或 ---end--- 标记');
    process.exit(1);
  }

  const contentLines = lines.slice(startIndex + 1, endIndex);

  const articles = contentLines.map(line => {
    const match = line.match(
      /^\[(.+?)\]\((.+?)\)(?:&emsp;|&nbsp;|\s)+发布时间：\s*([\d\-:]+)/
    );
    if (!match) return null;

    const [, title, url, datetime] = match;
    const slug = generateSlug(title, url);

    let categories = ['software'];
    if (url.includes('/hardware/')) categories = ['hardware'];
    if (url.includes('/network/')) categories = ['network'];

    return {
      title: title.trim(),
      url: url.trim(),
      date: datetime.replace(/-\d{2}:\d{2}$/, ''),
      datetime: datetime.trim(),
      slug,
      categories,
      tags: extractTagsFromTitle(title)
    };
  }).filter((article): article is typeof article & { title: string } => article !== null);

  writeFileSync('src/data/articles.json', JSON.stringify(articles, null, 2), 'utf-8');
  console.log(`已生成 ${articles.length} 篇文章的数据`);
}

parseReadme();