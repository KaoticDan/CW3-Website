function unsafeExecution(input) {
  // ruleid: website-no-dynamic-code-execution
  eval(input);
  // ruleid: website-no-dynamic-code-execution
  return new Function(input);
}

function requestHtml(request) {
  const input = request.nextUrl.searchParams.get('html');
  // ruleid: website-no-raw-react-html
  return <div dangerouslySetInnerHTML={{ __html: input }} />;
}

function trustedStyle() {
  // ok: website-no-raw-react-html
  return <style dangerouslySetInnerHTML={{ __html: ':root { --color: red; }' }} />;
}

function environment() {
  // ruleid: website-no-public-privileged-environment-key
  const secret = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY;
  // ok: website-no-public-privileged-environment-key
  const publishable = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;
  return { secret, publishable };
}

function unsafeTLS() {
  // ruleid: website-no-disabled-node-tls
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
}
