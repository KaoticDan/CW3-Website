export const requiredJobs=Object.freeze(['secrets','sast','site-checks']);
export function evaluateWebsiteCI(needs,expectedSha){
  const blockers=[];
  if(!/^[a-f0-9]{40}$/.test(expectedSha??''))blockers.push('Invalid expected source revision');
  for(const name of requiredJobs){
    const job=needs?.[name];
    if(job?.result!=='success')blockers.push(`${name}: successful result missing`);
    if(job?.outputs?.executed!=='true')blockers.push(`${name}: successful execution receipt missing`);
    if(job?.outputs?.source_sha!==expectedSha)blockers.push(`${name}: source revision mismatch`);
  }
  return{outcome:blockers.length?'blocked':'passed',scope:'website_ci_jobs_only',blockers};
}
if(process.env.EXPECTED_SOURCE_SHA!==undefined||process.env.REQUIRED_JOB_RESULTS!==undefined){
  let needs;try{needs=JSON.parse(process.env.REQUIRED_JOB_RESULTS??'');}catch{needs=null;}
  const result=evaluateWebsiteCI(needs,process.env.EXPECTED_SOURCE_SHA);
  console.log(result.outcome==='passed'?'Website CI checks passed. Release enforcement and hosted security remain separate.':'BLOCKED\n'+result.blockers.join('\n'));
  if(result.outcome!=='passed')process.exitCode=1;
}
