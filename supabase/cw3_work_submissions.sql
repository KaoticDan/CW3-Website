-- Apply after CW3 review, in project ykucsvjjynbmwfwvscbf.
create table if not exists public.cw3_work_submissions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null check (char_length(name) between 1 and 150),
  email text not null check (char_length(email) between 3 and 254),
  phone text not null check (char_length(phone) between 1 and 60)
);

alter table public.cw3_work_submissions enable row level security;
revoke all on public.cw3_work_submissions from anon, authenticated;
grant insert, select on public.cw3_work_submissions to service_role;

create index if not exists cw3_work_submissions_created_at_idx
  on public.cw3_work_submissions (created_at desc);
