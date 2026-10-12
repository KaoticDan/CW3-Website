const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
});

export async function POST(request) {
  if (request.headers.get('content-type')?.split(';')[0] !== 'application/json') {
    return json({ error: 'Expected JSON.' }, 415);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON.' }, 400);
  }
  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const email = typeof body.email === 'string' ? body.email.trim() : '';
  const phone = typeof body.phone === 'string' ? body.phone.trim() : '';
  if (!name || name.length > 150 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254 || !phone || phone.length > 60) {
    return json({ error: 'Please check your name, email, and phone number.' }, 400);
  }

  const base = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY;
  if (!base || !secret) return json({ error: 'Submissions are not configured yet.' }, 503);

  try {
    const response = await fetch(`${base.replace(/\/$/, '')}/rest/v1/cw3_work_submissions`, {
      method: 'POST',
      headers: {
        apikey: secret,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal',
      },
      body: JSON.stringify({ name, email, phone }),
    });
    if (!response.ok) return json({ error: 'Submission could not be saved.' }, 502);
    return json({ ok: true }, 201);
  } catch {
    return json({ error: 'Submission service unavailable.' }, 502);
  }
}

export function GET() {
  return json({ error: 'Method not allowed.' }, 405);
}
