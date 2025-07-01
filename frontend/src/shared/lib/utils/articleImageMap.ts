import Papa from 'papaparse';

export type ArticleImageMap = Record<string, string>;

export async function loadArticleImageMap(): Promise<ArticleImageMap> {
  return new Promise((resolve, reject) => {
    fetch('/article_image_url.csv')
      .then(res => res.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            const map: ArticleImageMap = {};
            for (const row of results.data as any[]) {
              if (row.article && row.image_url) {
                map[row.article] = row.image_url;
              }
            }
            resolve(map);
          },
          error: reject,
        });
      })
      .catch(reject);
  });
} 