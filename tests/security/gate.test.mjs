import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluateWebsiteCI,requiredJobs} from '../../scripts/security/check-website-ci.mjs';
const sha='a'.repeat(40);
const good=()=>Object.fromEntries(requiredJobs.map(name=>[name,{result:'success',outputs:{executed:'true',source_sha:sha}}]));
test('requires all successful jobs at the expected revision',()=>assert.equal(evaluateWebsiteCI(good(),sha).outcome,'passed'));
for(const state of ['failure','cancelled','skipped','pending'])test('blocks '+state,()=>{const jobs=good();jobs[requiredJobs[0]].result=state;assert.equal(evaluateWebsiteCI(jobs,sha).outcome,'blocked');});
test('blocks missing jobs, receipts, stale revisions and malformed input',()=>{for(const mutate of [j=>delete j[requiredJobs[0]],j=>delete j[requiredJobs[0]].outputs.executed,j=>j[requiredJobs[0]].outputs.source_sha='b'.repeat(40)]){const jobs=good();mutate(jobs);assert.equal(evaluateWebsiteCI(jobs,sha).outcome,'blocked');}for(const input of [null,{},[]])assert.equal(evaluateWebsiteCI(input,sha).outcome,'blocked');assert.equal(evaluateWebsiteCI(good(),'').outcome,'blocked');});
