export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    const escapeHtml = (s) =>
      String(s || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');

    // =====================================================
    // 0️⃣ ADMIN MANUAL UNBLOCK
    // =====================================================
    if (url.pathname === '/admin/unblock') {
      const student = url.searchParams.get('student');
      const adminKey = url.searchParams.get('key');

      if (adminKey !== env.ADMIN_SECRET) {
        return new Response('Unauthorized', { status: 403 });
      }

      if (!student) {
        return new Response('Missing student', { status: 400 });
      }

      await env.RATE_LIMIT_DB.delete(`student:${student}`);

      return new Response(`Student ${student} unblocked manually`, {
        status: 200,
        headers: { 'Content-Type': 'text/plain' }
      });
    }

    // =====================================================
    // 1️⃣ CAPTCHA PAGE (GET)
    // =====================================================
    if (url.pathname === '/captcha') {
      const student = url.searchParams.get('student');

      return new Response(
        `
        <html>
        <body>
          <h2>Complete CAPTCHA to unblock</h2>

          <form action="/captcha/verify" method="POST">
              <input type="hidden" name="student" value="${escapeHtml(
                student
              )}" />

              <div class="cf-turnstile" 
                data-sitekey="${env.TURNSTILE_SITE_KEY}">
              </div>

              <br/>

              <button type="submit">Verify</button>
          </form>

          <script src="https://challenges.cloudflare.com/turnstile/v0/api.js"></script>
        </body>
        </html>
        `,
        { status: 200, headers: { 'Content-Type': 'text/html' } }
      );
    }

    // =====================================================
    // 2️⃣ CAPTCHA VERIFY (POST)
    // =====================================================
    if (url.pathname === '/captcha/verify') {
      const formData = await request.formData();

      const student = formData.get('student');
      const cfResponse = formData.get('cf-turnstile-response');

      if (!student || !cfResponse) {
        return new Response('Bad Request', { status: 400 });
      }

      const verify = await fetch(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        {
          method: 'POST',
          body: new URLSearchParams({
            secret: env.TURNSTILE_SECRET_KEY,
            response: cfResponse
          })
        }
      );

      const result = await verify.json();

      if (!result.success) {
        return new Response('CAPTCHA failed. Try again.', { status: 403 });
      }

      await env.RATE_LIMIT_DB.delete(`student:${student}`);

      return Response.redirect('/', 302);
    }

    // =====================================================
    // 3️⃣ RATE LIMITING (run BEFORE fetching origin)
    // =====================================================
    const studentId = request.headers.get('student-id');
    const limit = 2; // >2 requests within TTL will be blocked

    if (studentId) {
      const key = `student:${studentId}`;
      const prev = Number((await env.RATE_LIMIT_DB.get(key)) || 0) || 0;
      const count = prev + 1;

      await env.RATE_LIMIT_DB.put(key, String(count), { expirationTtl: 60 });

      if (count > limit) {
        // Build external unblock URL (configurable via env)
        const unblockBase = env.UNBLOCK_URL || 'https://example.com/unblock';
        const unblockKey = env.UNBLOCK_KEY || 'fixstaticone';
        const unblockUrl = new URL(unblockBase);
        unblockUrl.searchParams.set('student', studentId);
        unblockUrl.searchParams.set('key', unblockKey);

        // Mode: 'redirect' (default) or 'fetch' to call external URL server-side
        const mode = (env.UNBLOCK_MODE || 'redirect').toLowerCase();

        if (mode === 'fetch') {
          // Fire-and-forget external call, then respond with 429
          fetch(unblockUrl.toString(), { method: 'GET' }).catch(() => {});
          return new Response('Too Many Requests', { status: 429 });
        }

        // Default: redirect user to the external unblock URL
        return Response.redirect(unblockUrl.toString(), 302);
      }
    }

    // Now the request is allowed, call origin
    const originResponse = await fetch(request);
    const headers = new Headers(originResponse.headers);

    // Add debug header to help testing (shows current count)
    if (studentId) {
      const cur = await env.RATE_LIMIT_DB.get(`student:${studentId}`);
      headers.set('X-Rate-Limit-Count', String(cur || 0));
    }

    return new Response(originResponse.body, {
      status: originResponse.status,
      headers
    });
  }
};
