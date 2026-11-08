const authHeader = "Basic " + btoa("demo:demo");

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: {
      Authorization: authHeader,
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("text/html")) return (await res.text()) as T;
  return res.json();
}

export { api };
