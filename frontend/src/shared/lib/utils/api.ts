const API_URL = import.meta.env.VITE_API_URL;

export async function apiPOST<T, R = any>(endpoint: string, body: T): Promise<R> {
    console.log('request')  
    console.log(API_URL + endpoint)
  const response = await fetch(API_URL + endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
  console.log('ok')



      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'API error');
      }
      
      const text = await response.text();
      if (!text) return {} as R;
      return JSON.parse(text) as R;
}

// export async function apiGET<T>(endpoint: string) {
    
      
// }